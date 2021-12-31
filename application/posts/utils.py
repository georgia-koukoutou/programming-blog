from application.models import Tag

def listToString(s):

   tag_string = ""

   for tag in s:
       tag_string += f"{tag.content}, "


   return tag_string[:len(tag_string)-2]

def stringToTagList(string):

    list = string.split(",")
    tag_list = []

    for element in list:
        if element.strip():
            tag_list.append(Tag(content=element.strip()))

    return tag_list

