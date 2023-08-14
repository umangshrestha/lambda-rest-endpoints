import json
from unittest import TestCase
from uuid import uuid4 as uuid

from tests.config import lambda_client


class LambdaBaseTestClass(TestCase):      
    def hello(self, payload):
        result = lambda_client.invoke(
            FunctionName='hello',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'pathParameters': payload
            })
        )
        self.assertEqual(result['StatusCode'], 200)
        output = json.loads(result['Payload'].read())
        output['body'] = json.loads(output['body'])
        return output

    def create_todo(self, _id):
        body = {
            "title": "Test",
            "description": "Test",
            "done": False,
            "deleted": False
        }
        if _id is not None:
            body['id'] = _id
        result = lambda_client.invoke(
            FunctionName='create_todo',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "body": body
            })
        )
        self.assertEqual(result['StatusCode'], 200)
        output = json.loads(result['Payload'].read())
        output['body'] = json.loads(output['body'])
        return output

    def delete_todo(self, _id):
        result = lambda_client.invoke(
            FunctionName='delete_todo',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "pathParameters": {
                    "id": _id
                }
            })
        )
        self.assertEqual(result['StatusCode'], 200)
        output = json.loads(result['Payload'].read())
        output['body'] = json.loads(output['body'])
        return output

    def update_todo(self, _id, title, description, done, deleted):
        result = lambda_client.invoke(
            FunctionName='update_todo',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "pathParameters": {
                    "id": _id,
                },
                "body": {
                    "title": title,
                    "description": description,
                    "done": done,
                    "deleted": deleted
                }
            })
        )
        self.assertEqual(result['StatusCode'], 200)
        output = json.loads(result['Payload'].read())
        output['body'] = json.loads(output['body'])
        return output

    def findall(self, limit=0, offset=5, deleted=False, done=False):
        result = lambda_client.invoke(
            FunctionName='get_todos',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "queryStringParameters": {
                    "limit": limit,
                    "offset": offset,
                    "deleted": deleted
                }
            })
        )
        self.assertEqual(result['StatusCode'], 200)
        output = json.loads(result['Payload'].read())
        output['body'] = json.loads(output['body'])
        return output

    def findone(self, _id):
        result = lambda_client.invoke(
            FunctionName='get_todo',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "pathParameters": {
                    "id": _id
                }
            })
        )
        self.assertEqual(result['StatusCode'], 200)
        output = json.loads(result['Payload'].read())
        output['body'] = json.loads(output['body'])
        return output


class TestLambda(LambdaBaseTestClass):

    def test_hello(self):
        output = self.hello({"name": "Lambda"})
        self.assertEqual(output, {
            "statusCode": 200,
            "body": {
                "message": "Hello, Lambda!"
            }
        })
      
    def test_hello_world(self):
        output = self.hello({})
        self.assertEqual(output, {
            "statusCode": 200,
            "body": {
                "message": "Hello, World!"
            }
        })


    def test_delete_todo_not_exist(self):
        output = self.delete_todo(str(uuid()))
        self.assertEqual(output, {
            "statusCode": 404,
            "body": {
                "error": "Todo not found!"
            }
        })

    def test_findone_todo_not_exist(self):
        output = self.findone(str(uuid()))
        self.assertEqual(output, {
            "statusCode": 404,
            "body": {
                "error": "Todo not found!"
            }
        })

    def test_update_todo_not_exist(self):
        output = self.update_todo(str(uuid()), "Test", "Test", False, False)
        self.assertEqual(output, {
            "statusCode": 404,
            "body": {
                "error": "Todo not found!"
            }
        })

    def test_create_todo_get_update_delete(self):
        _id = str(uuid())
        output = self.create_todo(_id)
        self.assertEqual(output, {
            "statusCode": 201,
            "body": {
                "id": _id,
                "message": "Todo created successfully!"
            }
        })      

        output = self.findone(_id)
        created_at = output['body'].pop('createdAt')
        updated_at = output['body'].pop('updatedAt')
        self.assertIsNotNone(created_at)
        self.assertIsNotNone(updated_at)
        self.assertEqual(output, {
            "statusCode": 200,
            "body": {
                "id": _id,
                "title": "Test",
                "description": "Test",
                "done": False,
                "deleted": False,
                "deletedAt": None,
            }
        })

        output = self.update_todo(_id, "Test2", "Test2", True, True)
        print
        self.assertEqual(output, {
            "statusCode": 200,
            "body": {
                "message": "Todo updated successfully!"
            }
        })

        output = self.findone(_id)
        self.assertEqual(created_at, output['body'].pop('createdAt'))
        self.assertIsNotNone(output['body'].pop('updatedAt'))
        self.assertIsNotNone(output['body'].pop('deletedAt'))
        self.assertIsNotNone(output['body'].pop('completedAt'))

        self.assertEqual(output, {
            "statusCode": 200,
            "body": {
                "id": _id,
                "title": "Test2",
                "description": "Test2",
                "done": True,
                "deleted": True,
            }
        })
        
        output = self.delete_todo(_id)
        self.assertEqual(output, {
            "statusCode": 200,
            "body": {
                "message": "Todo deleted successfully!"
            }
        })

    def test_create_todo_already_exist(self):
        _id = str(uuid())
        output = self.create_todo(_id)
        self.assertEqual(output, {
            "statusCode": 201,
            "body": {
                "id": _id,
                "message": "Todo created successfully!"
            }
        })
        output = self.create_todo(_id)
        self.assertEqual(output, {
            "statusCode": 409,
            "body": {
                "error": "Todo already exists!"
            }
        })
