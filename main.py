from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty,NumericProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from choose_image_func import choose_image
from product_size import findProductSize
from collections import defaultdict
from detect_product import product_detection

class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_press(self):
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, txt):
        self.text = txt


class RV(BoxLayout):
    data_items = ListProperty([])
    total = NumericProperty(0)
    products = {
        1001: ['Axe', 100,200],
        1002: ['Colgate Small', 50, 10],
        1003: ['Colgate Large', 100, 20],
        1004: ['Complan', 500, 250],
        1005: ['Dettol',200,70],
        1006: ['Diary Milk', 50, 20],
        1007: ['Fortune Oil', 500, 60],
        1008: ['Hamam Soap Small', 100, 30],
        1009: ['Hamam Soap Large', 200, 50],
        1010: ['Lays', 20,5],
        1011: ['Marie Gold small', 50, 5],
        1012: ['Marie Gold Big', 100, 10],
        1013: ['Ponds', 20, 40]
    }

    items_added = defaultdict(list)

    serial_no = 0
    product_ids = []
    serial_no_dict = {}

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

    def addData(self,product_id):
        if product_id in self.product_ids:
            index = self.serial_no_dict[product_id]
            self.items_added[index][3]+=1
            self.items_added[index][4]+=self.products[product_id][2]
            self.total+=self.products[product_id][2]
            pass
        else:
            self.serial_no+=1
            self.serial_no_dict[product_id]=self.serial_no
            self.product_ids.append(product_id)
            product_data  = self.products[product_id]
            self.items_added[self.serial_no].extend([product_data[0],product_id,product_data[1],1,product_data[2]])
            self.total+=product_data[2]
        self.data_items = []
        print(self.total)
        for i in range(1,len(self.items_added)+1):
            self.data_items.append(i)
            for j in range(5):
                self.data_items.append(self.items_added[i][j])

class TestApp(App):
    title = "Billing Application"
    file_path = ''
    product_img = Image(source='bg.png')
    right = None

    def callback(self, instance):
        print('The button <%s> is being pressed' % instance.text)

        self.file_path = choose_image()
        if(self.file_path!=None):
            self.product_img.source = self.file_path
            print(self.file_path)
            product_id = product_detection(self.file_path)
            self.right.addData(product_id)
        else:
            print('No File Selected')

    def build(self):
        layout = BoxLayout(orientation='horizontal')
        left = BoxLayout(orientation='vertical')
        self.right = RV()

        image_layout = BoxLayout(orientation='vertical')
        choose_btn_layout = BoxLayout(orientation='vertical', size=(100,100),size_hint=(None, None))

        # choose_btn_layout.padding = [50,10,10,10]
        left.add_widget(image_layout)
        left.spacing=10
        left.padding = [10,10,10,10]


        image_layout.padding = [30,60,20,60]

        choose_image_btn = Button(text='Choose Image', size=(150,100),size_hint=(None,None))
        choose_image_btn.bind(on_press=self.callback)
        choose_btn_layout.padding = [220,10,10,10]

        self.product_img.allow_stretch = True
        self.product_img.keep_ratio = False
        self.product_img.size_hint_x = 0.95
        self.product_img.size_hint_y = 0.8

        image_layout.add_widget(self.product_img)
        choose_btn_layout.add_widget(choose_image_btn)
        left.add_widget(choose_btn_layout)
        layout.add_widget(left)
        layout.add_widget(self.right)
        return layout

if __name__ == "__main__":
    TestApp().run()