from django import template
register = template.Library()

@register.simple_tag
def setvar(val=None):
  return val

@register.simple_tag
def nam1var(val=None):
  return int(val) + 1

num = 0
@register.simple_tag
def namvar(val=None):
  global num
  num = num + int(val)
  return num

@register.simple_tag
def delnamvar():
  global num
  num = 0

num2 = 0
@register.simple_tag
def namvar2(val2=None):
  global num2
  num2 = num2 + int(val2)
  return num2

@register.simple_tag
def delnamvar2():
  global num2
  num2 = 0

num3 = 0
@register.simple_tag
def namvar3(val3=None):
  global num3
  num3 = num3 + int(val3)
  return num3

@register.simple_tag
def delnamvar3():
  global num3
  num3 = 0

num4 = 0
@register.simple_tag
def namvar4(val4=None):
  global num4
  num4 = num4 + int(val4)
  return num4

@register.simple_tag
def delnamvar4():
  global num4
  num4 = 0