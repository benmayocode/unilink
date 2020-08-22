from django.shortcuts import render
from django.http import JsonResponse
import ast
from todo.models import ToDo, RowOrder
import datetime
from django import db
db.connections.close_all()

def get_to_do_list(current_user):
    """
    takes the current user, returns their todo list as a list of dicts
    checks the current users history to see if they've save their list order
    """

    # get the order of rows that we have in the db, parse from sting to list with ast
    try:
        last_order_id = RowOrder.objects.filter(username=current_user).latest('id').id
        order_obj = RowOrder.objects.filter(username=current_user).filter(id=last_order_id).values()[0]
        order_as_list = ast.literal_eval(order_obj.get('row_order'))
    except:
        print ('We dont have a record for this person')
        order_as_list = []

    # instantiate a list
    to_dos = []
    # get all of the to-dos
    to_do_table = ToDo.objects.filter(username=current_user)
    # this is all pretty messy, probably a nicer way to do this with a better list comprehension technique
    task_text_list = [item.task_text for item in to_do_table]
    date_created_list = [item.created_date for item in to_do_table]
    date_due_list = [item.due_date for item in to_do_table]
    task_id_list = [item.task_id for item in to_do_table]
    completed_list = []
    for item in to_do_table:
        # not sure about working with bools between python, sqlite and javascript, so I'll use 1 and 0
        if item.completed is True:   completed_list.append(1)
        if item.completed is False:   completed_list.append(0)

    to_do_list = list(zip(task_text_list, date_created_list, date_due_list, completed_list, task_id_list))

    # check to see if we have a saved order
    # if we do we will build the list of dicts in the correct order
    # this is inefficient - would find a better way to do this - this will do the up to the square of n rows as an if check

    # print ('order list: {}').format(order_as_list)
    if len(order_as_list) > 0:
        for pos in order_as_list:
            for to_do in to_do_list:
                if int(to_do[4]) == int(pos):
                    to_dos.append(
                        {'text': to_do[0], 'date_created': str(to_do[1]), 'date_due': str(to_do[2]), 'completed': to_do[3],
                         'task_id': to_do[4]})
                    continue

    else:
        # we don't have a previous order - just build the list
        for to_do in to_do_list:
            to_dos.append({'text': to_do[0], 'date_created': str(to_do[1]), 'date_due': str(to_do[2]), 'completed':to_do[3], 'task_id':to_do[4]})

    return to_dos

def query_set_to_dict(query):
    for q in query:
        print ('\t', q.values())

def remove_item_from_list_history(current_user, to_remove):
    obj = RowOrder.objects.filter(username=current_user)
    obj_values = obj.values()[0]
    order_as_list = ast.literal_eval(obj_values.get('row_order'))
    order_as_list.remove(to_remove)
    order_as_string = str(order_as_list)

    update_row = RowOrder.objects.get(id=obj_values.get('id'))
    update_row.row_order = order_as_string
    update_row.save()

def update_order(current_user, new_order):
    obj = RowOrder.objects.filter(username=current_user)
    obj_values = obj.values()[0]

    update_row = RowOrder.objects.get(id=obj_values.get('id'))
    update_row.row_order = new_order
    update_row.save()

def add_item_to_row_order(current_user, to_add, existing_row_order):
    new_row_order = existing_row_order
    new_row_order.append(to_add)

    # get the numer of rows in the table
    num_rows_for_user = RowOrder.objects.filter(username=current_user).count()

    if num_rows_for_user == 0:
        # this user does not have a record
        # check to see if we have any rows at all
        num_rows_overall = RowOrder.objects.count()

        if num_rows_overall == 0:
            # no records at all in the table, use 1 as the id
            record_id = 1
        if num_rows_overall > 0:
            # we do have records, so use the next largest for the user
            record_id = RowOrder.objects.latest('id').id + 1

        new_item = RowOrder(username=str(current_user), id=record_id, row_order=new_row_order)
        new_item.save()


    if num_rows_for_user > 0:
        # we've created a record for this user already - get its ID and update the record it
        last_order_id = RowOrder.objects.filter(username=current_user).latest('id').id
        existing_item = RowOrder.objects.get(id=last_order_id)
        existing_item.row_order = new_row_order
        existing_item.save()


def index(request):

    data_in_str = request.body.decode("UTF-8")
    current_user = request.user

    # @to_do this is not great way to do it
    if len(data_in_str) > 0:
        data_in = ast.literal_eval(data_in_str)

        # get the function rquired
        function = data_in.get('func')

        if function == 'addJob':
            # add a new job to the to do list
            text = data_in.get('text')
            due_date = data_in.get('dueDate')
            existing_row_order = data_in.get('rowOrder')
            new_item = ToDo(task_text=text, completed=False, created_date=datetime.date.today(), due_date=due_date, username=current_user)
            new_item.save()

            new_task_id = new_item.task_id
            obj = ToDo.objects.filter(task_id=new_task_id).values()[0]
            add_item_to_row_order(current_user, new_task_id, existing_row_order)

            return JsonResponse(obj, safe=False)

        if function == 'removeJob':
            taskID = data_in.get('taskID')
            ToDo.objects.get(task_id=taskID).delete()
            remove_item_from_list_history(current_user, taskID)

        if function == 'toggleChecked':
            taskID = data_in.get('taskID')
            checked = data_in.get('checked')
            if checked == 1:    checked_bool = True
            if checked == 0:    checked_bool = False
            t = ToDo.objects.get(task_id=taskID)
            t.completed = checked_bool
            t.save()

        if function == 'reorderTasks':
            new_order = str(data_in.get('rowOrder'))
            update_order(current_user, new_order)

    to_dos = get_to_do_list(current_user)

    return render(request, 'todo.html', {'to_dos':to_dos})

