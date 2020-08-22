function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getRowOrder(){
        rowOrder = []
        $('#sortable tr').each(function() {
            var rowID = $(this).find(".taskIDCell").html();
            console.log()
            rowInt = parseInt(rowID)
            if (rowInt > 0){
            rowOrder.push(parseInt(rowID))
            }
         });
         console.log(rowOrder)
         return rowOrder
}

function addTableRow(item){
        console.log(item)
        $('#sortable').append(`
                <tr class='ui-sortable-handle' id=rowID${item.task_id}>
                <td class="taskIDCell" data-id="${item.task_id}">${item.task_id}</td>
                <td>${item.task_text}</td>
                <td>${item.created_date}</td>
                <td>${item.due_date}</td>
                <td><input class="checkbox" type="checkbox"></td>
                <td><button class="btn btn-danger btn-small" onclick=removeJob(${item.task_id})>Remove</button> </td>
           </tr>`);
}

function addJob(){
        text = $('#taskText').val()
        rowOrder = getRowOrder()
        dueDate = $('#taskDueDate').val()
        var csrftoken = getCookie('csrftoken');
        const data = {
            func: 'addJob',
            text: text,
            dueDate: dueDate,
            rowOrder: rowOrder,
        };
        fetch('/todo/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify(data),
        })
        .then((response) => response.json())
        .then((data) => {
        addTableRow(data)
        })
    }

function removeJob(taskID){
        var csrftoken = getCookie('csrftoken');
        const data = {
            func: 'removeJob',
            taskID: taskID,
        };

        fetch('/todo/', {
                method: 'POST', // or 'PUT'
                headers: {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify(data),
        })
    $('#rowID'+taskID).remove();
    }

function reorderTasks(){
        var csrftoken = getCookie('csrftoken');

        rowOrder = getRowOrder()

        const data = {
            func: 'reorderTasks',
            rowOrder: rowOrder,
        };

        fetch('/todo/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify(data),
        })
    }

function toggleChecked(taskID, checked){
        var csrftoken = getCookie('csrftoken');
        const data = {
            func: 'toggleChecked',
            taskID: taskID,
            checked: checked,
        };

        fetch('/todo/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify(data),
        })
    }


function toggleCheckBox(taskID){

    if ($('#checkBoxID'+taskID).is(":checked"))
    {
        console.log('checked')
        toggleChecked(taskID, 1)
    }
    else
    {
        console.log('not checked')
        toggleChecked(taskID, 0)

    }


}

makeSortable()