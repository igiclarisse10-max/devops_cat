"""
Unit tests for the To-Do List application (app.py)
Tests cover Flask routes and database operations
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


@pytest.fixture
def sample_task(client):
    """Create a sample task for testing"""
    with app.app_context():
        task = Task(title="Test Task", completed=False)
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        db.session.expunge(task)
    with app.app_context():
        return Task.query.get(task_id)


class TestHomeRoute:
    """Test cases for the home route"""
    
    def test_home_route_returns_200(self, client):
        """Test that home route returns status 200"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_home_route_returns_html(self, client):
        """Test that home route returns HTML content"""
        response = client.get('/')
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data


class TestGetTasksAPI:
    """Test cases for GET /api/tasks endpoint"""
    
    def test_get_tasks_empty_list(self, client):
        """Test retrieving tasks when database is empty"""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_get_tasks_with_existing_tasks(self, client, sample_task):
        """Test retrieving tasks when tasks exist"""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) >= 1
        assert data[0]['title'] == 'Test Task'
        assert data[0]['completed'] is False
    
    def test_get_tasks_returns_correct_structure(self, client, sample_task):
        """Test that each task has correct structure"""
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        assert 'id' in data[0]
        assert 'title' in data[0]
        assert 'completed' in data[0]


class TestCreateTaskAPI:
    """Test cases for POST /api/tasks endpoint"""
    
    def test_create_task_success(self, client):
        """Test successfully creating a new task"""
        response = client.post('/api/tasks', 
            data=json.dumps({'title': 'New Task'}),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'New Task'
        assert data['completed'] is False
        assert 'id' in data
    
    def test_create_task_persists_to_database(self, client):
        """Test that created task is stored in database"""
        client.post('/api/tasks',
            data=json.dumps({'title': 'Persistent Task'}),
            content_type='application/json'
        )
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['title'] == 'Persistent Task'
    
    def test_create_multiple_tasks(self, client):
        """Test creating multiple tasks"""
        for i in range(3):
            client.post('/api/tasks',
                data=json.dumps({'title': f'Task {i}'}),
                content_type='application/json'
            )
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        assert len(data) == 3


class TestUpdateTaskAPI:
    """Test cases for PATCH /api/tasks/<id> endpoint"""
    
    def test_update_task_completed_status(self, client, sample_task):
        """Test updating a task's completed status"""
        with app.app_context():
            task_id = sample_task.id
        response = client.patch(f'/api/tasks/{task_id}',
            data=json.dumps({'completed': True}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['completed'] is True
    
    def test_update_nonexistent_task_returns_404(self, client):
        """Test that updating nonexistent task returns 404"""
        response = client.patch('/api/tasks/9999',
            data=json.dumps({'completed': True}),
            content_type='application/json'
        )
        assert response.status_code == 404
    
    def test_update_task_preserves_title(self, client, sample_task):
        """Test that updating status doesn't change title"""
        with app.app_context():
            task_id = sample_task.id
            original_title = sample_task.title
        client.patch(f'/api/tasks/{task_id}',
            data=json.dumps({'completed': True}),
            content_type='application/json'
        )
        
        response = client.get(f'/api/tasks')
        data = json.loads(response.data)
        assert data[0]['title'] == original_title


class TestDeleteTaskAPI:
    """Test cases for DELETE /api/tasks/<id> endpoint"""
    
    def test_delete_task_success(self, client, sample_task):
        """Test successfully deleting a task"""
        with app.app_context():
            task_id = sample_task.id
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 204
    
    def test_delete_task_removes_from_database(self, client, sample_task):
        """Test that deleted task is removed from database"""
        with app.app_context():
            task_id = sample_task.id
        client.delete(f'/api/tasks/{task_id}')
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        assert len(data) == 0
    
    def test_delete_nonexistent_task_returns_404(self, client):
        """Test that deleting nonexistent task returns 404"""
        response = client.delete('/api/tasks/9999')
        assert response.status_code == 404


class TestTaskModel:
    """Test cases for Task database model"""
    
    def test_task_creation(self, client):
        """Test creating a task instance"""
        with app.app_context():
            task = Task(title="Model Test Task", completed=False)
            assert task.title == "Model Test Task"
            assert task.completed is False
    
    def test_task_default_completed_is_false(self, client):
        """Test that new tasks default to not completed"""
        with app.app_context():
            task = Task(title="Default Test")
            db.session.add(task)
            db.session.flush()
            assert task.completed is False
