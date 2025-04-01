"""
API resource endpoints for the szn-libeaas package.

This module provides classes for interacting with specific API endpoints.
"""
from typing import Dict, List, Optional, Any, Union


class ResourceManager:
    """
    Base class for API resource managers.
    
    This class provides common functionality for specific resource endpoints.
    """
    
    def __init__(self, client):
        """
        Initialize the resource manager.
        
        Args:
            client: API client instance
        """
        self.client = client


class UsersManager(ResourceManager):
    """Manager for user resources."""
    
    BASE_PATH = "users"
    
    def list(self, page: int = 1, per_page: int = 20, **params) -> Dict[str, Any]:
        """
        List users with pagination.
        
        Args:
            page: Page number
            per_page: Number of results per page
            **params: Additional query parameters
            
        Returns:
            Dictionary with user data and pagination info
        """
        params.update({
            'page': page,
            'per_page': per_page
        })
        
        response = self.client.get(self.BASE_PATH, params=params)
        return response.data
    
    def get(self, user_id: str) -> Dict[str, Any]:
        """
        Get a user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User data
        """
        response = self.client.get(f"{self.BASE_PATH}/{user_id}")
        return response.data
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            data: User data
            
        Returns:
            Created user data
        """
        response = self.client.post(self.BASE_PATH, json_data=data)
        return response.data
    
    def update(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a user.
        
        Args:
            user_id: User ID
            data: User data to update
            
        Returns:
            Updated user data
        """
        response = self.client.put(f"{self.BASE_PATH}/{user_id}", json_data=data)
        return response.data
    
    def delete(self, user_id: str) -> None:
        """
        Delete a user.
        
        Args:
            user_id: User ID
        """
        self.client.delete(f"{self.BASE_PATH}/{user_id}")


class ProjectsManager(ResourceManager):
    """Manager for project resources."""
    
    BASE_PATH = "projects"
    
    def list(self, page: int = 1, per_page: int = 20, **params) -> Dict[str, Any]:
        """
        List projects with pagination.
        
        Args:
            page: Page number
            per_page: Number of results per page
            **params: Additional query parameters
            
        Returns:
            Dictionary with project data and pagination info
        """
        params.update({
            'page': page,
            'per_page': per_page
        })
        
        response = self.client.get(self.BASE_PATH, params=params)
        return response.data
    
    def get(self, project_id: str) -> Dict[str, Any]:
        """
        Get a project by ID.
        
        Args:
            project_id: Project ID
            
        Returns:
            Project data
        """
        response = self.client.get(f"{self.BASE_PATH}/{project_id}")
        return response.data
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new project.
        
        Args:
            data: Project data
            
        Returns:
            Created project data
        """
        response = self.client.post(self.BASE_PATH, json_data=data)
        return response.data
    
    def update(self, project_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a project.
        
        Args:
            project_id: Project ID
            data: Project data to update
            
        Returns:
            Updated project data
        """
        response = self.client.put(f"{self.BASE_PATH}/{project_id}", json_data=data)
        return response.data
    
    def delete(self, project_id: str) -> None:
        """
        Delete a project.
        
        Args:
            project_id: Project ID
        """
        self.client.delete(f"{self.BASE_PATH}/{project_id}")


class TasksManager(ResourceManager):
    """Manager for task resources."""
    
    BASE_PATH = "tasks"
    
    def list(self, project_id: Optional[str] = None, page: int = 1, per_page: int = 20, **params) -> Dict[str, Any]:
        """
        List tasks with pagination.
        
        Args:
            project_id: Optional project ID to filter tasks
            page: Page number
            per_page: Number of results per page
            **params: Additional query parameters
            
        Returns:
            Dictionary with task data and pagination info
        """
        params.update({
            'page': page,
            'per_page': per_page
        })
        
        if project_id:
            params['project_id'] = project_id
        
        response = self.client.get(self.BASE_PATH, params=params)
        return response.data
    
    def get(self, task_id: str) -> Dict[str, Any]:
        """
        Get a task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task data
        """
        response = self.client.get(f"{self.BASE_PATH}/{task_id}")
        return response.data
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new task.
        
        Args:
            data: Task data
            
        Returns:
            Created task data
        """
        response = self.client.post(self.BASE_PATH, json_data=data)
        return response.data
    
    def update(self, task_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a task.
        
        Args:
            task_id: Task ID
            data: Task data to update
            
        Returns:
            Updated task data
        """
        response = self.client.put(f"{self.BASE_PATH}/{task_id}", json_data=data)
        return response.data
    
    def delete(self, task_id: str) -> None:
        """
        Delete a task.
        
        Args:
            task_id: Task ID
        """
        self.client.delete(f"{self.BASE_PATH}/{task_id}")
    
    def complete(self, task_id: str) -> Dict[str, Any]:
        """
        Mark a task as complete.
        
        Args:
            task_id: Task ID
            
        Returns:
            Updated task data
        """
        response = self.client.post(f"{self.BASE_PATH}/{task_id}/complete")
        return response.data


class DocumentsManager(ResourceManager):
    """Manager for document resources."""
    
    BASE_PATH = "documents"
    
    def list(self, project_id: Optional[str] = None, page: int = 1, per_page: int = 20, **params) -> Dict[str, Any]:
        """
        List documents with pagination.
        
        Args:
            project_id: Optional project ID to filter documents
            page: Page number
            per_page: Number of results per page
            **params: Additional query parameters
            
        Returns:
            Dictionary with document data and pagination info
        """
        params.update({
            'page': page,
            'per_page': per_page
        })
        
        if project_id:
            params['project_id'] = project_id
        
        response = self.client.get(self.BASE_PATH, params=params)
        return response.data
    
    def get(self, document_id: str) -> Dict[str, Any]:
        """
        Get a document by ID.
        
        Args:
            document_id: Document ID
            
        Returns:
            Document data
        """
        response = self.client.get(f"{self.BASE_PATH}/{document_id}")
        return response.data
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new document.
        
        Args:
            data: Document data
            
        Returns:
            Created document data
        """
        response = self.client.post(self.BASE_PATH, json_data=data)
        return response.data
    
    def update(self, document_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a document.
        
        Args:
            document_id: Document ID
            data: Document data to update
            
        Returns:
            Updated document data
        """
        response = self.client.put(f"{self.BASE_PATH}/{document_id}", json_data=data)
        return response.data
    
    def delete(self, document_id: str) -> None:
        """
        Delete a document.
        
        Args:
            document_id: Document ID
        """
        self.client.delete(f"{self.BASE_PATH}/{document_id}")


class AnalyticsManager(ResourceManager):
    """Manager for analytics resources."""
    
    BASE_PATH = "analytics"
    
    def get_usage(self, start_date: str, end_date: str, **params) -> Dict[str, Any]:
        """
        Get usage data for a date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            **params: Additional query parameters
            
        Returns:
            Usage data
        """
        params.update({
            'start_date': start_date,
            'end_date': end_date
        })
        
        response = self.client.get(f"{self.BASE_PATH}/usage", params=params)
        return response.data
    
    def get_summary(self, period: str = 'month', **params) -> Dict[str, Any]:
        """
        Get summary analytics.
        
        Args:
            period: Time period ('day', 'week', 'month', 'year')
            **params: Additional query parameters
            
        Returns:
            Summary analytics data
        """
        params.update({'period': period})
        
        response = self.client.get(f"{self.BASE_PATH}/summary", params=params)
        return response.data