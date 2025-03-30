from typing import Union
from copy import copy, deepcopy

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, Grid
from textual.widgets import Label, SelectionList, DataTable, Footer, Input, Button, RichLog
from textual.widgets.selection_list import Selection
from textual.screen import Screen, ModalScreen

from components import SelectionSwapList
from living_objects import Ausgabe, Einzahlung, MockDb, Transfer

table_filter = ['amount', 'category', 'note', 'payee', 'date']
#* test balloon for filtering and sorting by order in the array


class Header(Horizontal):
    def compose(self) -> ComposeResult:
        yield Label("Dashboard")
        yield Label("Spent")
        yield Label("Income")
        yield Label("Categories")
        yield Label("Graphs")
        yield Label("Options")


class FilterMenu(ModalScreen[tuple]):

    BINDINGS = [
        Binding(key="escape", action="close_filter_menu", show=False),
        Binding(key="enter", action="accept_filter_menu", show=False),
    ]

    def __init__(self, filter_config: dict):
        self.filter_config = filter_config
        super().__init__()

    def compose(self) -> ComposeResult:
        self.widget_selections = SelectionSwapList(id="question", classes="max_width_height")

        with Grid(id="dialog"):
            yield self.widget_selections
            with Horizontal(id="buttons_two"):
                yield Button("Cancel", id="btn_cancel")
                yield Button("Accept", id="btn_accept")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#question").border_title = "Filter Table Columns"
        #options = [Selection(key, i, value) for i, (key, value) in enumerate(self.filter_config.items())]
        options = [Selection(key, key, value) for key, value in self.filter_config.items()]
        self.widget_selections.clear_options()
        self.widget_selections.add_options(options)

    @on(Button.Pressed, "#btn_cancel")
    def cancel_filter(self):
        self.dismiss([])

    @on(Button.Pressed, "#btn_accept")
    def accept_filter(self):
        ordered_columns = copy(self.widget_selections.selected)
        self.dismiss(ordered_columns)

    def action_close_filter_menu(self):
        self.dismiss([])


class Gemeinschaftskonto(App):
    CSS_PATH = 'gemeinschaft.tcss'

    BINDINGS = [
        Binding(key='q', action="quit", description="Quit the app"),
        Binding(key='a', action="add_row", description="Adds new entry from blank slate"),
        Binding(key='t', action="add_template", description="Adds new entry from template", show=False),
        Binding(key='r', action="remove_row", description="Deletes current row"),
        Binding(key='f', action="filter_menu", description="Filters tables"),
        Binding(key='u', action="update_table", description="Repopulate Table from DB"),
        Binding(key='c', action="copy_row", description="Copies current row", show=False)
    ]

    def __init__(self, db_connector: MockDb):
        self.db = db_connector
        self.filter_table = table_filter
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Header()
            with Horizontal():
                yield DataTable(id='spend', zebra_stripes=True, cursor_type="row")
            yield Input(value="", placeholder="Debug Text here", id="debug_txt", disabled=True)
            yield Footer()

    def on_mount(self) -> None:
        self.action_update_table()

    def action_update_table(self):
        data = self.db.get_all_data()
        table = self.query_one("#spend")
        table.clear(columns=True)
        all_column = Transfer.props()
        select_column = all_column  # default
        if self.filter_table:
            select_column = []
            for key in self.filter_table:
                if key in all_column:
                    select_column.append(key)
        table.add_columns(*select_column)
        for id, each in (data.items()):
            temp_array = each.str_dict()
            select_row = []
            for key in select_column:
                if key in temp_array:
                    select_row.append(temp_array[key])
                else:
                    select_row.append("") # should never happen
            table.add_row(*select_row, key=id, label=id)

    def action_remove_row(self):
        # todo: check if table empty
        dt = self.query_one("#spend")
        row_key, column_key = dt.coordinate_to_cell_key(dt.cursor_coordinate)
        dt.remove_row(row_key)
        self.db.remove_data(row_key.value)
        self.write_debug(f"Next Index: {self.db.add_random_mock()}")

    def action_filter_menu(self):

        def handle_filter_response(filter_tables: list| None) -> None:
            self.write_debug(str(filter_tables))
            if not filter_tables:
                return
            self.filter_table = filter_tables
            self.action_update_table()

        options = {x: True for x in self.filter_table}
        options = options | {x: False for x in Transfer.props() if x not in self.filter_table}
        self.app.push_screen(FilterMenu(options), handle_filter_response)

    def write_debug(self, message: str):
        text = self.query_one("#debug_txt")
        text.value = message

    def _build_table(self, target_id: str, data: Union[list[Ausgabe], list[Einzahlung]]):
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], Ausgabe):  # crude testy
            self._build_table_ausgabe(target_id, data)
        return None


if __name__ == "__main__":
    my_db = MockDb("doesntmatter where")
    app = Gemeinschaftskonto(my_db)
    app.run()


# Cyberpunk color scheme
eins = {
 	"black": "#00060e",
	"dark_yellow": "#9a9f17",
	"yellow": "#fee801",
	"lighblue": "#54c1e6",
	"cobold": "#39c4b6"
}

cp77 = {
    "yellow": "#F9F500",
    "red": "#F91642",
    "lightblue": "#31D8F2",
    "darkerblue": "#2C4FFF",
    "pink": "#FF00F0",
    "light_red": "#FE1F58",
    "green": "#31D55E",
    "orange": "#FB9B05",
    "other_orange": "#F03E21",
    "thired_orange": "#F38624",
    "purple": "#9F29E7",
    "blue": "#246FD5",
    "white": "#D6D0D0"
}