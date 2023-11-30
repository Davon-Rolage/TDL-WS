import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Todo


class TodoConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
    
    def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            if self.user.username in ['ohana']:
                self.room_group_name = 'todo_ohana'
                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
                )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        if not self.user.is_authenticated:
            return
        
        text_data_json = json.loads(text_data)
        event_type = text_data_json['type']
        
        async def group_send_event(event_type, data):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': event_type,
                    **data
                }
            )
        
        if event_type == 'todo.add_task':
            task_title = text_data_json['task']
            new_task = Todo.objects.create(title=task_title)
            async_to_sync(group_send_event)('todo.add_task', {
                'task_id': new_task.pk,
                'task_title': new_task.title
            })
        elif event_type == 'todo.toggle_complete':
            task_id = text_data_json['task_id']
            task = Todo.objects.get(pk=task_id)
            task.completed = not task.completed
            task.save()
            async_to_sync(group_send_event)('todo.toggle_complete', {
                'task_id': task_id
            })
        elif event_type == 'todo.delete_task':
            task_id = text_data_json['task_id']
            Todo.objects.get(pk=task_id).delete()
            async_to_sync(group_send_event)('todo.delete_task', {
                'task_id': task_id
            })
        elif event_type == 'todo.delete_completed':
            Todo.objects.filter(completed=True).delete()
            async_to_sync(group_send_event)('todo.delete_completed', {})
        elif event_type == 'todo.delete_all':
            Todo.objects.all().delete()
            async_to_sync(group_send_event)('todo.delete_all', {})
    
    def todo_add_task(self, event):
        self.send(text_data=json.dumps(event))
        
    def todo_toggle_complete(self, event):
        self.send(text_data=json.dumps(event))
        
    def todo_delete_task(self, event):
        self.send(text_data=json.dumps(event))
    
    def todo_delete_completed(self, event):
        self.send(text_data=json.dumps(event))
    
    def todo_delete_all(self, event):
        self.send(text_data=json.dumps(event))
    