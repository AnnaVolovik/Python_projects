import json
import os
import time

from flask import request, render_template

from app import app
from ..static.tree_like_data import content, structure


@app.route('/get_tree_like_content', methods=['GET'])
def get_tree_like_content():
    """ Return input data: content & the structure of the output """
    filename = os.path.join(app.root_path, 'static', 'tree_like_data_js.json')
    # f = open(filename)
    # content = f.read()
    # content = json.loads(filename)
    # return json.dumps(content)
    return json.dumps(dict(content=dict(content=content), structure=structure))


@app.route('/restructure_tree_like_data', methods=['GET'])
def restructure_tree_like_data():
    """Return restructured data """
    # if request.method == 'GET':
    #     return render_template('project_four.html',
    #                            start_data=content,
    #                            output_struct=structure,
    #                            result=None)

    # elif request.method == 'POST':

    # start_time = time.time()
    new_content = get_new_structure(request_data_payload=content,
                                    request_struct=structure
                                    )
    # time = round((time.time() - start_time), 3)

    return json.dumps(new_content)

    # return render_template('project_four.html',
    #                        start_data=content,
    #                        output_struct=structure,
    #                        result=new_content, time=time)

# helper functions

def get_structure(structure, col_id, header, columns, tree, level, parent_id):
    """
    Get information about columns, including tables with multilevel headers,
    Get header cells

    :param structure: structure - list of objects [{}, {}]
    :param col_id: int - column id
    :param header: dict() - a helper container that stores full information about columns - it is required to process
            data but too excessive to be returned to the front end
    :param columns: list() - a list to store information about columns
    :param tree: dict() - is supposed to store information like {level: {cells : [], rows : []}}
    :param level: int - 0, is incremented for children column elements of multilevel headers
    :param parent_id: int - is used for multilevel headers
    :return:
    """

    if not level in tree:
        tree[level] = dict(
            cells=[],
            row=dict(parentId=None, childIds=[], open=True, level=0, id=level, type='headerRow')
        )

    level_els = []  # set to an empty list in each cycle
    params = ['width_value', 'width_type', 'col_name', 'aggr', 'col_type', 'table_options',
              'round_value', 'hidden', 'editable', 'display']

    i = 0  # for multi-level headers we do not show the first child
    for struct_el in structure:

        i += (1 if level > 0 else 0)

        attributes = {}
        parent = False
        value = struct_el.get('description')

        if struct_el.get('children', []):  # parent node

            parent = True

            col_id += 1
            col = dict(id=col_id)

            columns, col_id, header, children, tree,  = \
                get_structure(
                    structure=struct_el.get('children', []),
                    col_id=col_id - 1,
                    header=header,
                    columns=columns,
                    tree=tree,
                    level=level + 1,
                    parent_id=col_id
                )
            childIds = [x.get('id') for x in children[1:]]

            # parent inherits first child's parameters as it's located right underneath
            for param in params:
                attributes[param] = children[0].get(param)

        else:  # child node
            for param in params:
                attributes[param] = struct_el.get(param)
            childIds = []

            col_id += 1
            col = dict(id=col_id)

        col['parentId'] = parent_id
        col['open'] = True
        col['level'] = level
        col['childIds'] = childIds

        for param in ['width_value', 'width_type', 'col_name', 'aggr', 'display', 'col_type', 'round_value']:
            col[param] = attributes[param]
        level_els.append(col)
        if not (i == 1 and level > 0):
            columns.append(col)

        cell = dict(column=col_id,
                    value=value,
                    type='headerCell',
                    row=level
                    )
        tree[level]['cells'].append(cell)

        header_info = dict(column=col_id)
        if not parent:
            for param in ['display', 'col_name', 'editable', 'aggr', 'round_value', 'col_type']:
                header_info[param] = attributes[param]

            header.append(header_info)

    return columns, col_id, header, level_els, tree


def get_content(start_el, cells, header, current_row, rows, parent_row, level):
    """
    Processing body of the table - recursively going through rows and computing node values
    :param start_el: dict() - content element object
    :param cells: list() - container to keep cells as a list of object for each row
    :param header: objects list() - helper paramter that contains information about each column
    :param current_row: int - current row id - is incremented with each row
    :param rows: list() - container to keep rows as objects
    :param parent_row: int - parent row id
    :param level: int - level of nesting
    :return: dict()
    """

    current_row += 1  # the row of the element we entered with
    level += 1  # everytime we call the function we go one nested level further
    sub_row = None

    totals = dict(cells=[], rows=[])  # to keep track of children rows for aggregation

    if start_el.get('children', []):  # parent node

        sub_row = current_row  # keep separate value for children rows id

        for child in start_el.get('children'):

            cells, cell_level, sub_row, row_level, rows = \
                get_content(child, cells, header, sub_row, rows, current_row, level)
            totals['cells'].append(cell_level)
            totals['rows'].append(row_level)

    cell_level = []  # working on cells, go by each row and each column (using helper header parameter)

    for header_col in header:
        if start_el.get('children', []):
            # get aggregated values of totals for parent nodes
            value = get_value(header_col, totals['cells'])
        else:  # get value from the content element for children
            value = start_el.get(header_col.get('col_name'))

            # make sure the value looks correct for some types
            if header_col.get('col_type') in ['bool', 'bool_plus']:
                value = bool(value)
            elif header_col.get('col_type') in ['num', 'solnum']:
                if value == 0:
                    value = None
                elif value:
                    value = round(value, int(header_col.get('round_value')))

        cell_type = get_type(header_col, start_el)

        # get the value of hierarchical cells according to its display rules
        if cell_type == 'hierarchyCell':
            display = header_col.get('display', None)

            if not display or display == 5:
                value = f"{start_el.get('code','')} - {start_el.get('description','')}"
            elif display == 1:
                value = start_el.get('code', '')
            elif display == 2:
                value = start_el.get('summary', '')
            elif display == 3:
                value = start_el.get('description', '')
            elif display == 4:
                value = f"{start_el.get('code','')} - {start_el.get('summary','')}"

        cell_level.append(dict(value=value, type=cell_type, row=current_row, column=header_col.get('column')))

    cells.append(cell_level)

    # processing rows
    row_level = dict(
        parentId=parent_row,
        childIds=[] if not totals.get('rows') else [r['id'] for r in totals.get('rows')],
        open=True,
        level=level,
        id=current_row,
        type='listRow'
    )
    rows.append(row_level)

    # return one row on each child
    return cells, cell_level, sub_row if sub_row else current_row, row_level, rows


def get_new_structure(request_data_payload, request_struct):

    # set containers for rows and cells, where we are going to store data
    cells = []
    rows = []

    # get information about table struct and columns
    columns, i, header, level_els, tree = \
        get_structure(structure=request_struct, col_id=-1, header=[],
                      columns=[], tree={}, level=0, parent_id=None)
    header = sorted(header, key=lambda x: x['column'])
    columns = sorted(columns, key=lambda x: x['id'])

    # form cells for multi-level headers - some cells should stay empty
    for level in tree:
        cell_level = []
        for col in range(max(x['column'] for x in header) + 1):
            cell = next((x for x in tree.get(level).get('cells') if x['column'] == col), None)
            if not cell:  # add an empty cell
                cell = dict(column=col, value=None, type='headerCell', row=level)
            cell_level.append(cell)
        cells.append(cell_level)
        rows.append(tree.get(level).get('row'))

    # in this variable all general information about the table will be keps
    request_info = dict(
        fixedRowCount=len(rows),  # header rows are fixed
        fixedColumnCount=1,  # the first column is fixed
    )

    # if there is aggregation in at least one column, leaving space for the total result row
    total_row = 0
    sub_row = len(cells) - 1
    if any(x in ['sum', 'min', 'max', 'count', 'avg'] for x in [h['aggr'] for h in header]) \
            or 'bool_plus' in [h.get('col_type') for h in header]:
        total_row = len(cells)
        sub_row = total_row
    totals = dict(cells=[])

    # forming table body
    for el in request_data_payload:
        # going recursively through each element on the highest level
        # keep information in the totals variable for the main result row
        cells, cell_level, sub_row, row_level, rows = \
            get_content(
                start_el=el,
                cells=cells,
                header=header,
                current_row=sub_row,
                rows=rows,
                parent_row=None,
                level=-1,
            )
        totals['cells'].append(cell_level)

    # main result
    cell_level = []

    if total_row:
        for header_col in header:
            if header_col.get('aggr') == 'null':
                if header_col['column'] == 0:
                    value = 'Total result'
                elif header_col.get('col_type') == 'bool_plus':
                    value = get_value(header_col, totals['cells'])
                else:
                    value = None
            else:  # only for columns with aggregation
                value = get_value(header_col, totals['cells'])
            cell_level.append(dict(value=value, type='mainResultCell', column=header_col.get('column'), row=total_row))

        cells.append(cell_level)
        rows.append(dict(
            parentId=None,
            childIds=[],
            open=True,
            level=0,
            id=total_row,
            type='mainResultRow'))

    # sort containers
    cells = sorted(cells, key=lambda x: x[0]['row'])
    rows = sorted(rows, key=lambda x: x['id'])

    # a number of rows without the fixed ones
    request_info['rowCount'] = len(rows) - request_info['fixedRowCount']
    # a number of columns without the fixed ones
    request_info['columnCount'] = len(columns) - request_info['fixedColumnCount']
    request_info['highestRowsId'] = [r.get('id') for r in rows if r.get('level') == 0]
    request_info['highestColumnsId'] = [c.get('id') for c in columns if c['level'] == 0]
    request_info['rowDeepestLevel'] = max([x['level'] for x in rows])
    request_info['columnDeepestLevel'] = max(x['level'] for x in columns)

    return dict(
        cells=cells,
        rows=rows,
        columns=columns,
        request_info=request_info
    )


def get_value(header_col, total_cells, key='column'):
    """
    Функция агрегации значений на узлах формы ввода
    :param header_col: описание колонки
    :param key: 'column' / 'col_name' - забирать значения из ячеек по алиасу или положению колонки (по умолчанию)
    :param cells: массив с массивами ячеек каждой строки, являющейся прямым ребенком
    [[{}, {] ячейки строки],[ячейки другой строки],[]]- каждой строке соответствует массив
    :return: значение на узле в зависимости от типа игрегации и значений прямых детей в этой колонке
    """

    value = None

    if header_col.get('col_type') == 'bool':  # обработка checkobox

        value = None

        # для последних элементов (детей), Null превращается в False, чтобы отрисовывались пустые checkbox
        # проверяется непосредственно в теле form_body

    if header_col.get('col_type') == 'bool_plus':

        total = [x.get('value', None) for cell_level in total_cells
                 for x in cell_level if x.get(key) == header_col.get(key)]

        value = False if False in total else True

    elif header_col.get('aggr') in ['sum', 'min', 'max', 'count', 'avg']:
        # обработка других типов ячеек с агрегацией

        if header_col.get('col_type') in ['num', 'solnum']:
            round_value = header_col.get('round_value', None)
            try:
                round_value = int(round_value)
            except:
                round_value = 1

            total = [float(x.get('value')) for cell_level in total_cells
                     for x in cell_level if x.get(key) == header_col.get(key) and x.get('value')]

            if header_col.get('aggr') == 'sum':
                value = sum(total)

            elif header_col.get('aggr') == 'min':
                if total:
                    # replace Nones for calculations
                    total = [x if x else 0 for x in total]
                    value = min(total)
                else:
                    value = None
            elif header_col.get('aggr') == 'max':
                if total:
                    total = [x if x else 0 for x in total]
                    value = max(total)
                else:
                    value = None
            elif header_col.get('aggr') == 'avg':
                if total:
                    total = [x if x else 0 for x in total]
                    value = sum(total) / len(total)
                else:
                    value = None
            elif header_col.get('aggr') == 'count':
                value = len([x for x in total if x])

            if value == 0:
                value = None  # не отрисовывать нули
            else:
                value = round(value, round_value)

        elif header_col.get('col_type') == 'datetype':
            # для данных типа datetype доступна агрегация типа max и min
            total = [x.get('value') for cell_level in total_cells for x in cell_level if
                     x.get(key) == header_col.get(key) and x.get('value')]

            # TODO может нужно перевести в тип datetime и обратно. Протестировать
            if header_col.get('aggr') == 'min':
                value = min(total)
            elif header_col.get('aggr') == 'max':
                value = max(total)
        else:  # не агрегируются значения типа 'all' и 'key', даже если агрегация указана
            value = None
    else:  # если агрегация не указана, или равна 'null', то значение на родительском узле = None
        value = None

    return value


def get_type(header_col, start_el):

    cell_type = 'simpleCell'  # тип по умолчанию

    if header_col['column'] == 0:
        # первый столбец иерархичной структуры - тип hierarchyCell
        cell_type = 'hierarchyCell'

    elif header_col.get('col_type') == 'bool':
        # Если узловые и общий результат есть (aggr = count):
        # 1. Когда editable = True, то тип checkbox;
        # 2. Когда editable = False, то тип disabled;

        # родительские - зависят от аггрегации - simple или
        if start_el.get('children', []):

            # if header_col.get('aggr', 'null') == 'count':
            #     if header_col.get('editable'):
            #         cell_type = 'checkboxCell'
            #     else:
            #         cell_type = 'disabledCheckBox'
            # else:
            cell_type = 'simpleCell'
        else:
            if header_col.get('editable') and start_el.get('edit', None) is not False:
                cell_type = 'checkboxCell'
            else:
                cell_type = 'disabledCheckBox'

    elif header_col.get('col_type') == 'bool_plus':

        if start_el.get('children', []):
            if header_col.get('editable'):
                cell_type = 'checkboxCell'
            else:
                cell_type = 'disabledCheckBox'
        else:
            if start_el.get('edit', None) is not False:
                cell_type = 'checkboxCell'
            else:
                cell_type = 'disabledCheckBox'
    # можно еще смотреть на то, является ли он родителем - на узлах тип должен быть simpleCell
    # ставим тип selectorCell, только если ячейка редактируемая - то есть на нее можно кликнуть и выбрать справочник
    # если нет, например на узлах, ставим simpleCell

    elif start_el.get('edit', None) is not False and header_col.get('editable') and not start_el.get('children', []):
        # elif start_el.get('edit') and header_col.get('editable') and not start_el.get('children', []):
        if header_col['col_type'] == 'key':
            cell_type = 'selectorCell'
        elif header_col.get('col_type') == 'datetype':
            cell_type = 'dateCell'
        elif header_col.get('col_type') in ['num', 'solnum', 'all']:
            cell_type = 'inputCell'

    return cell_type


