from conftest import user, task
import pytest

def test_add_post(task):
    add = task.add_task() 
    assert add.status_code == 200
    pid = add.json().get('id')
    get_post = task.get_task_by_id(pid)
    des = add.json().get('description')
    tit = add.json().get('title')
    assert get_post.json() == {'completed': False, 'description': des, 'id': pid, 'title': tit}

def test_edit_post(task):
    add = task.add_task()
    pid = add.json().get('id')
    get_post = task.get_task_by_id(pid)
    edit = task.edit_task(pid)
    assert edit.status_code == 200
    des = add.json().get('description')
    tit = add.json().get('title')
    assert get_post.json() == {'completed': False, 'description': des, 'id': pid, 'title': tit}

def test_delete_post(task):
    add = task.add_task()
    pid = add.json().get('id')
    dele = task.delete_task(pid)
    get_post = task.get_task_by_id(pid)
    assert dele.status_code == 204
    assert get_post.json() == {'detail': 'Task not found'}
    