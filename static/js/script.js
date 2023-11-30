const taskInputDom = $('#input-box');
const buttonAddTask = $('#btn-add-task');
const buttonDeleteAll = $('#btn-delete-all');
const buttonDeleteCompleted = $('#btn-delete-completed');
let taskListContainer = $('#list-container');
taskInputDom.focus();


function resetEventListeners() {
    // Click enter to add task
    taskInputDom.on('keypress', function(e) {
        if (e.key === 'Enter') {  // enter, return
            buttonAddTask.click();
        }
    });
    // Add task
    buttonAddTask.on('click', function(e) {
        const task = taskInputDom.val();
        if (task !== '') {
            todoSocket.send(JSON.stringify({
                'type': 'todo.add_task',
                'task': task
            }));
            taskInputDom.val('');
            taskInputDom.focus();
        }
    });
    // Toggle complete
    $(".task-text").on('click', function(e) {
        const taskId = this.id;
        todoSocket.send(JSON.stringify({
            'type': 'todo.toggle_complete',
            'task_id': taskId
        }));
    });
    // Delete task
    $(".delete-x").on('click', function(e) {
        const taskId = this.id;
        todoSocket.send(JSON.stringify({
            'type': 'todo.delete_task',
            'task_id': taskId
        }));
    });
    // Delete completed tasks
    buttonDeleteCompleted.on('click', function(e) {
        const completedTasksNum = $(".task-text.checked").parent().length;
        if (completedTasksNum > 0) {
            todoSocket.send(JSON.stringify({
                'type': 'todo.delete_completed'
            }));
        };
    });
    // Delete all tasks
    buttonDeleteAll.on('click', function(e) {
        const tasksNum = taskListContainer.children().length;
        if (tasksNum > 0) {
            todoSocket.send(JSON.stringify({
                'type': 'todo.delete_all'
            }));
        }
    });
}


// Delete task hover effect
$(".delete-x").hover(function(e) {
    const task = $(e.target.parentNode.parentNode).find(".task-text");
    task.css("background-color", "rgba(255, 0, 0, 0.25)");
}, function(e) {
    const task = $(e.target.parentNode.parentNode).find(".task-text");
    task.css("background-color", "");
})

function addTask(taskId, taskTitle) {
    const task = $(`<div class="row align-items-center justify-content-between" id="row_${taskId}">
        <div class="col-1">
            <span class="delete-x text-center" id="${taskId}">X</span>
        </div>
        <div class="task-text col-9 py-2 text-end" id="${taskId}">
            <span class="pl-3">${taskTitle}</span>
        </div>
        <div class="task-img col-1 px-0" id="${taskId}">
            <img class="checkbox" src="/static/images/unchecked.png">
        </div>
    </div>`);
    taskListContainer.prepend(task);
    resetEventListeners();
}

function toggleComplete(taskId) {
    const task = $(`#row_${taskId}`);
    const taskText = task.find(".task-text");
    const checkedImage = task.find(".task-img").find("img");

    taskText.toggleClass("checked");
    if (taskText.hasClass("checked")) {
        checkedImage.attr("src", "../static/images/checked.png");
    } else {
        checkedImage.attr("src", "../static/images/unchecked.png");
    }
}

// Connect to websocket
let todoSocket = null;
function connect() {
    todoSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/todo/'
    );

    todoSocket.onopen = function(e) {
        console.log("Successfully opened todo socket");
    }

    todoSocket.onmessage = function(e) {
        const data = JSON.parse(e.data)

        switch (data.type) {
            case 'todo.add_task':
                addTask(data.task_id, data.task_title);
                break;
            case 'todo.toggle_complete':
                toggleComplete(data.task_id);
                break;
            case 'todo.delete_task':
                $(`#row_${data.task_id}`).remove();
                break;
            case 'todo.delete_completed':
                $(".task-text.checked").parent().remove();
                break;
            case 'todo.delete_all':
                taskListContainer.children().remove();
                break;
            default:
                console.error("Unknown message type:", data.type);
                break;
        }
    };

    todoSocket.onclose = function(e) {
        console.error("Todo socket closed unexpectedly. Trying to reconnect in 5s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 5000);
    };

    todoSocket.onerror = function(err) {
        console.log("Websocket encountered an error:", err.message);
        console.log("Closing the socket.")
        todoSocket.close();
    };
}
connect();
resetEventListeners();
