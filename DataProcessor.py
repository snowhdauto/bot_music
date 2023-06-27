

def GetRows(markup,data,countcolmn):
    li = []
    for i in data:
        li.append(i)
        if len(li)==countcolmn:
            markup.row(*li)
            li=[]
    if len(li) > 0:
        markup.row(*li)
    del li