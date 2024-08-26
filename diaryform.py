import npyscreen as nps

class DiaryLogForm(nps.Form):
    def create(self):
        self.chemical = self.add(nps.TitleText, name='Chemical', w_id="chemical")
        self.quantity = self.add(nps.TitleText, name='Quantity', w_id="quantity")
        self.date = self.add(nps.TitleDateCombo, name='Date', w_id="date")

    def afterEditing(self):
        self.parentApp.setNextForm(None)

class FormApp(nps.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", DiaryLogForm, name='New diary log')

def init_diary_form():
    app = FormApp()
    app.run()
    return app.getForm("MAIN")