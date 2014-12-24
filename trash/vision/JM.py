import toolbox.EasyGame as game

#response = Confirm.get('Are you sure you want to exit without saving ?','WARNING ...')

min_examples = 10
examples =[1, 2, 3, 4]

def _get_dialog_label():
        return "When teaching a new gesture you need to provide " + str(min_examples) +\
            " examples, but you only provided " + str(len(examples)) +". Do you" +\
            " wish to abort and lose those changes?"

res = game.confirm(_get_dialog_label(), 'warning', mode=2)
print res