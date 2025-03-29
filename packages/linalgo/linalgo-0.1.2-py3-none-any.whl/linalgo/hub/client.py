# pylint: skip-file
from typing import List
import io
import warnings
from enum import Enum

from contextlib import closing
import csv
import requests
import zipfile

from linalgo.annotate.models import (
    Annotation, Annotator, Corpus, Document, Entity, Task, Schedule
)
from linalgo.annotate import models, serializers
from linalgo.annotate.serializers import AnnotationSerializer, DocumentSerializer


class AssignmentType(Enum):
    REVIEW = 'R'
    LABEL = 'A'


class AssignmentStatus(Enum):
    ASSIGNED = 'A'
    COMPLETED = 'C'


class LinalgoClient:

    endpoints = {
        'annotators': 'annotators',
        'annotations': 'annotations',
        'corpora': 'corpora',
        'documents': 'documents',
        'entities': 'entities',
        'task': 'tasks',
        'annotations-export': 'annotations/export',
        'documents-export': 'documents/export',
        'organizations': 'organizations'
    }

    def __init__(self, token, api_url="http://localhost:8000"):
        self.api_url = api_url
        self.access_token = token

    def get(self, url, query_params={}):
        headers = {'Authorization': f"Token {self.access_token}"}
        res = requests.get(url, headers=headers, params=query_params)
        if res.status_code == 401:
            raise Exception(f"Authentication failed. Please check your token.")
        if res.status_code == 404:
            raise Exception(f"{url} not found.")
        elif res.status_code != 200:
            raise Exception(
                f"Request returned status {res.status_code}, {res.content}")
        return res.json()

    def post(self, url, data=None, files=None, json=None):
        headers = {'Authorization': f"Token {self.access_token}"}
        res = requests.post(url, data=data, json=json, files=files, headers=headers)
        if 200 <= res.status_code < 300:
            return res
        if res.status_code == 401:
            raise Exception(f"Authentication failed. Please check your token.")
        elif res.status_code == 404:
            raise Exception(f"{url} not found.")
        else:
            raise Exception(
                f"Request returned status {res.status_code}, {res.content}")

    def request_csv(self, url, query_params={}):
        headers = {'Authorization': f"Token {self.access_token}"}
        # stream the file
        with closing(requests.get(url, stream=True,
                                  headers=headers, params=query_params)) as res:
            if res.status_code == 401:
                raise Exception(
                    f"Authentication failed. Please check your token.")
            if res.status_code == 404:
                raise Exception(f"{url} not found.")
            elif res.status_code != 200:
                raise Exception(f"Request returned status {res.status_code}")
            root = zipfile.ZipFile(io.BytesIO(res.content))
            f = root.namelist()
            if len(f):
                d = csv.DictReader(io.TextIOWrapper(root.open(f[0]), 'utf-8'))
            else:
                d = []
            return d

    def get_current_annotator(self):
        """Returns the current annotator."""
        url = f"{self.api_url}/{self.endpoints['annotators']}/me/"
        return Annotator(**self.get(url))

    def create_corpus(self, corpus: Corpus, organization: models.Organization):
        """Creates a new corpus.
        
        Parameters
        ----------
        corpus: Corpus
        organization: Organization
        
        Returns
        -------
        Corpus
        """
        url = f"{self.api_url}/{self.endpoints['corpora']}/"
        serializer = serializers.CorpusSerializer(corpus)
        data = serializer.serialize()
        data['organization'] = organization.id
        res = self.post(url, data=data)
        return models.Corpus(**res.json())
    
    def add_documents(self, documents: List[models.Document]):
        """Add the documents provided"""
        url = f"{self.api_url}/{self.endpoints['documents']}/import_documents/"
        serializer = serializers.DocumentSerializer(documents)
        f = io.StringIO()
        keys = ['id', 'uri', 'content','corpus_id']
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(serializer.serialize())
        csv_content = f.getvalue()
        files = {'fileKey': ('data.csv', csv_content.encode('utf-8'), 'text/csv')}
        return self.post(url, files=files)
    
    def get_next_document(self, task_id: str):
        url = f"{self.api_url}/tasks/{task_id}/next_document/"
        return Document(**self.get(url))
    

    def get_corpora(self):
        res = self.get(self.endpoints['corpora'])
        corpora = []
        for js in res['results']:
            corpus_id = js['id']
            corpus = self.get_corpus(corpus_id)
            corpora.append(corpus)
        return corpora
    
    def get_organizations(self):
        url = f"{self.api_url}/{self.endpoints['organizations']}/"
        orgs = []
        for data in self.get(url)['results']:
            org = models.Organization(**data)
            orgs.append(org)
        return self.get(url)['results']
    
    def get_organization(self, org_id: str):
        url = f"{self.api_url}/{self.endpoints['organizations']}/{org_id}/"
        data = self.get(url)
        return models.Organization(**data)

    def get_corpus(self, corpus_id):
        url = f"{self.api_url}/{self.endpoints['corpora']}/{corpus_id}/"
        res = self.get(url)
        corpus = Corpus.from_dict(res)
        # corpus = Corpus(name=res['name'], description=res['description'])
        documents = self.get_corpus_documents(corpus_id)
        corpus.documents = documents
        return corpus

    def get_corpus_documents(self, corpus_id):
        url = f"{self.api_url}/documents/?page_size=1000&corpus={corpus_id}"
        res = self.get(url)
        documents = []
        for d in res['results']:
            document = Document.from_dict(d)
            documents.append(document)
        return documents

    def get_tasks(self, task_ids=[]):
        url = "tasks/"
        tasks = []
        res = self.get(url)
        if len(task_ids) == 0:
            for js in res['results']:
                task_ids.append(js['id'])
        for task_id in task_ids:
            task = self.get_task(task_id)
            tasks.extend(task)
        return tasks

    def get_task_documents(self, task_id):
        query_params = {
            'task_id': task_id,
            'output_format': 'zip',
            'only_documents': True
        }
        api_url = "{}/{}/".format(
            self.api_url, self.endpoints['documents-export'])
        records = self.request_csv(api_url, query_params)
        data = [Document.from_dict(row) for row in records]
        return data

    def get_task_annotations(self, task_id):
        query_params = {'task_id': task_id, 'output_format': 'zip'}
        api_url = "{}/{}/".format(
            self.api_url, self.endpoints['annotations-export'])
        records = self.request_csv(api_url, query_params)
        data = [Annotation.from_dict(row) for row in records]
        return data

    def get_task(self, task_id, verbose=False, lazy=False):
        task_url = "{}/{}/{}/".format(
            self.api_url, self.endpoints['task'], task_id)
        if verbose:
            print(f'Retrivieving task with id {task_id}...')
        task_json = self.get(task_url)
        task = Task.from_dict(task_json)
        if lazy:
            return task
        if verbose:
            print('Retrieving annotators...', end=' ')
        task.annotators = self.get_annotators(task)
        if verbose:
            print(f'({len(task.annotators)} found)')
        if verbose:
            print('Retrieving entities...', end=' ')
        params = {'tasks': task.id, 'page_size': 1000}
        if verbose:
            print(f'({len(task.entities)} found)')
        entities_url = "{}/{}".format(self.api_url, self.endpoints['entities'])
        entities_json = self.get(entities_url, params)
        task.entities = [Entity.from_dict(e) for e in entities_json['results']]
        if verbose:
            print('Retrieving documents...', end=' ')
        task.documents = self.get_task_documents(task_id)
        if verbose:
            print(f'({len(task.documents)} found)')
        if verbose:
            print('Retrieving annotations...', end=' ')
        task.annotations = self.get_task_annotations(task_id)
        if verbose:
            print(f'({len(task.annotations)} found)')
        n = len([a for d in task.documents for a in d.annotations])
        if len(task.annotations) != n:
            warnings.warn('Some annotations have no associated document.')
        return task

    def get_annotators(self, task):
        if isinstance(task, str):
            task = Task(unique_id=task)
        params = {'tasks': task.id, 'page_size': 1000}
        annotators_url = "{}/{}/".format(
            self.api_url, self.endpoints['annotators'])
        res = self.get(annotators_url, params)
        annotators = []
        for a in res['results']:
            annotator = Annotator.from_dict(a)
            annotators.append(annotator)
        return annotators

    def create_annotator(self, annotator):
        url = "{}/{}/".format(self.api_url, self.endpoints['annotators'])
        annotator_json = {
            'id': annotator.id,
            'name': annotator.name,
            'model': str(annotator.model),
            'owner': annotator.owner
        }
        res = self.post(url, json=annotator_json)
        if res.status_code != 201:
            raise Exception(res.content)
        res = res.json()
        annotator.annotator_id = res['id']
        annotator.owner = res['owner']
        return annotator

    def add_annotators_to_task(self, annotators, task):
        endpoint = self.endpoints['task']
        url = f"{self.api_url}/{endpoint}/{task.id}/add_annotators/"
        payload = [annotator.id for annotator in annotators]
        return self.post(url, json=payload)

    def create_annotations(self, annotations):
        url = "{}/{}/import_annotations/".format(
            self.api_url, self.endpoints['annotations'])
        serializer = AnnotationSerializer(annotations)
        payload = serializer.serialize()
        res = self.post(url, json=payload)
        return res

    def delete_annotations(self, annotations):
        url = "{}/{}/bulk_delete/".format(self.api_url,
                                          self.endpoints['annotations'])
        headers = {'Authorization': f"Token {self.access_token}"}
        annotations_ids = [annotation.id for annotation in annotations]
        res = requests.delete(url, json=annotations_ids, headers=headers)
        if res.status_code != 204:
            raise Exception(res.content)
        return res

    def assign(
        self,
        document: Document,
        annotator: Annotator,
        task: Task,
        reviewee=None,
        assignment_type=AssignmentType.LABEL.value
    ):
        doc_status = {
            'status': AssignmentStatus.ASSIGNED.value,
            'type': assignment_type,
            'document': document.id,
            'annotator': annotator.id,
            'task': task.id,
            'reviewee': reviewee
        }
        url = self.api_url + '/document-status/'
        res = self.post(url, data=doc_status)
        return res

    def unassign(self, status_id):
        headers = {'Authorization': f"Token {self.access_token}"}
        url = f"{self.api_url}/document-status/{status_id}/"
        res = requests.delete(url, headers=headers)
        return res

    def get_schedule(self, task):
        query_params = {'task': task.id, 'page_size': 1000}
        schedules = []
        next_url = f"{self.api_url}/document-status/"
        while next_url:
            res = self.get(next_url, query_params=query_params)
            next_url = res['next']
            schedules.extend(Schedule(**s) for s in res['results'])
        return schedules

    def add_document(self, doc: Document, corpus: Corpus):
        url = f"{self.api_url}/corpora/{corpus.id}/add_document/"
        payload = DocumentSerializer(doc).serialize()
        return self.post(url, data=payload)
    
    def complete_document(self, doc, task):
        endpoint = self.endpoints['task']
        url = f"{self.api_url}/{endpoint}/{task.id}/complete_document/"
        return self.post(url, data={'document': doc.id})


__all__ = ['LinalgoClient']