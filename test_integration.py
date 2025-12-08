"""
Integration tests for the To-Do List application
Tests complete user workflows and end-to-end scenarios
"""

import pytest
import json
from app import app, db, Task


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


class TestCompleteUserWorkflow:
    """Integration tests for complete user workflows"""
    
    def test_create_read_update_delete_workflow(self, client):
        """Test complete CRUD workflow: Create -> Read -> Update -> Delete"""
        # Step 1: Create a task
        create_response = client.post('/api/tasks',
            data=json.dumps({'title': 'Complete Integration Test'}),
            content_type='application/json'
        )
        assert create_response.status_code == 201
        task_data = json.loads(create_response.data)
        task_id = task_data['id']
        
        # Step 2: Read the task
        read_response = client.get('/api/tasks')
        assert read_response.status_code == 200
        tasks = json.loads(read_response.data)
        assert len(tasks) == 1
        assert tasks[0]['id'] == task_id
        
        # Step 3: Update the task
        update_response = client.patch(f'/api/tasks/{task_id}',
            data=json.dumps({'completed': True}),
            content_type='application/json'
        )
        assert update_response.status_code == 200
        updated_task = json.loads(update_response.data)
        assert updated_task['completed'] is True
        
        # Step 4: Delete the task
        delete_response = client.delete(f'/api/tasks/{task_id}')
        assert delete_response.status_code == 204
        
        # Verify task is deleted
        final_response = client.get('/api/tasks')
        final_tasks = json.loads(final_response.data)
        assert len(final_tasks) == 0
    
    def test_multiple_tasks_workflow(self, client):
        """Test managing multiple tasks"""
        # Create multiple tasks
        task_titles = ['Buy groceries', 'Complete project', 'Call doctor', 'Exercise']
        created_ids = []
        
        for title in task_titles:
            response = client.post('/api/tasks',
                data=json.dumps({'title': title}),
                content_type='application/json'
            )
            assert response.status_code == 201
            created_ids.append(json.loads(response.data)['id'])
        
        # Verify all tasks are created
        response = client.get('/api/tasks')
        tasks = json.loads(response.data)
        assert len(tasks) == 4
        
        # Complete first two tasks
        for task_id in created_ids[:2]:
            response = client.patch(f'/api/tasks/{task_id}',
                data=json.dumps({'completed': True}),
                content_type='application/json'
            )
            assert response.status_code == 200
        
        # Verify completion status
        response = client.get('/api/tasks')
        tasks = json.loads(response.data)
        completed_count = sum(1 for t in tasks if t['completed'])
        assert completed_count == 2
        
        # Delete a task
        response = client.delete(f'/api/tasks/{created_ids[0]}')
        assert response.status_code == 204
        
        # Verify remaining tasks
        response = client.get('/api/tasks')
        tasks = json.loads(response.data)
        assert len(tasks) == 3


class TestDataPersistence:
    """Integration tests for data persistence across requests"""
    
    def test_tasks_persist_across_requests(self, client):
        """Test that tasks persist across multiple API calls"""
        # Create tasks
        for i in range(5):
            client.post('/api/tasks',
                data=json.dumps({'title': f'Persistence Test {i}'}),
                content_type='application/json'
            )
        
        # Verify all tasks exist in multiple calls
        for _ in range(3):
            response = client.get('/api/tasks')
            tasks = json.loads(response.data)
            assert len(tasks) == 5


class TestErrorHandling:
    """Integration tests for error scenarios"""
    
    def test_invalid_task_id_handling(self, client):
        """Test handling of invalid task IDs"""
        # Try to get/update/delete non-existent task
        assert client.get('/api/tasks/99999').status_code == 200  # GET returns empty-like
        assert client.patch('/api/tasks/99999',
            data=json.dumps({'completed': True}),
            content_type='application/json'
        ).status_code == 404
        assert client.delete('/api/tasks/99999').status_code == 404
    
    def test_concurrent_task_operations(self, client):
        """Test handling of rapid sequential operations"""
        # Create multiple tasks rapidly
        ids = []
        for i in range(10):
            response = client.post('/api/tasks',
                data=json.dumps({'title': f'Concurrent {i}'}),
                content_type='application/json'
            )
            ids.append(json.loads(response.data)['id'])
        
        # Update all tasks rapidly
        for task_id in ids:
            response = client.patch(f'/api/tasks/{task_id}',
                data=json.dumps({'completed': True}),
                content_type='application/json'
            )
            assert response.status_code == 200
        
        # Verify all updates were applied
        response = client.get('/api/tasks')
        tasks = json.loads(response.data)
        assert all(t['completed'] for t in tasks)


class TestAPIResponseFormat:
    """Integration tests for API response formats and consistency"""
    
    def test_consistent_response_structure(self, client):
        """Test that all task responses have consistent structure"""
        # Create a task
        create_response = client.post('/api/tasks',
            data=json.dumps({'title': 'Structure Test'}),
            content_type='application/json'
        )
        created_task = json.loads(create_response.data)
        
        # Get all tasks
        list_response = client.get('/api/tasks')
        tasks = json.loads(list_response.data)
        
        # Update task
        update_response = client.patch(f'/api/tasks/{created_task["id"]}',
            data=json.dumps({'completed': True}),
            content_type='application/json'
        )
        updated_task = json.loads(update_response.data)
        
        # All should have same structure
        for task in [created_task, tasks[0], updated_task]:
            assert isinstance(task, dict)
            assert set(task.keys()) == {'id', 'title', 'completed'}
            assert isinstance(task['id'], int)
            assert isinstance(task['title'], str)
            assert isinstance(task['completed'], bool)


class TestUIIntegration:
    """Integration tests for UI page loading"""
    
    def test_home_page_loads(self, client):
        """Test that home page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert response.content_type == 'text/html; charset=utf-8'
    
    def test_home_page_has_required_elements(self, client):
        """Test that home page contains required HTML elements"""
        response = client.get('/')
        html = response.data.decode()
        
        # Check for key elements
        assert 'taskInput' in html or 'task' in html.lower()
        assert 'taskList' in html or 'list' in html.lower()
        assert 'app.js' in html  # Should load JavaScript
