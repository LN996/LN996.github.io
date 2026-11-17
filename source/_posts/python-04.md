---
title: 面向对象编程
date: 2026-11-04 09:00:00
tags:
  - Python
  - 面向对象
categories:
  - Python学习笔记
---
> 本文是「Python全栈学习中心」系列笔记之一,配套可刷题的本地工具(获取方式见文末)。

---

## 📖 面向对象

> 🎬 对应课程:Python基础 第7章(类、三大特性、绑定方法、反射、元类)

### 1. 类与对象(类属性 vs 实例属性)
> 🎬 对应视频:P352~P357

**类是**模板**,对象是实例;`__init__` 在实例化时自动执行;**类属性所有实例共享,实例属性每个对象独有一份**。**

- 定义:`class 类名:`(大驼峰命名);实例化 `p = 类名(参数)` 自动触发 `__init__`
- 实例方法的第一个参数 self 就是**当前实例**,实例属性靠 `self.x = ...` 绑定在对象上
- 类属性写在类里方法外,所有实例共享;实例属性只属于一个对象
- 取值先找**实例属性**,找不到再找类属性;`实例.属性 = 值` 是给实例新增属性,**不会改类属性**
- 对象属性可以动态增删:`p.age = 18`、`del p.age`

```python
class Student:
    school = "老男孩"   # 类属性,所有实例共享

    def __init__(self, name):
        self.name = name   # 实例属性,每个对象独有

s1 = Student("alex")
s2 = Student("wusir")
s1.school = "AA"   # 给 s1 新增实例属性,不影响类属性
print(s1.school, s2.school, Student.school)   # AA 老男孩 老男孩
```

*类属性 vs 实例属性*

### 2. 三大特性:封装 / 继承 / 多态
> 🎬 对应视频:P370~P371、P380

****封装**隐藏细节、**继承**复用扩展(用 super 复用父类初始化)、**多态**同一调用不同表现;Python 是鸭子类型,不强制继承统一父类。**

- 封装的弱私有:单下划线 `_x` 约定不外部使用;双下划线 `__x` 触发**名称改写**成 `_类名__x`
- 继承:`class Son(Father)`,子类找不到的属性方法去父类找;同名方法直接重写覆盖
- `super().__init__(...)` 在子类里复用父类的初始化,避免重复代码
- 多继承按 **MRO**(C3 线性化)从左到右查找,`类名.__mro__` 可查看顺序
- 多态/鸭子类型:不关心对象是什么类型,只要有那个方法就能调用

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):   # 重写父类方法
        return "汪汪"

def make_sound(animal):
    print(animal.speak())   # 多态:不关心具体类型

make_sound(Dog("旺财"))   # 汪汪
```

### 3. 组合与依赖
> 🎬 对应视频:P362~P363、P379

**继承是“**是**”的关系(狗是动物),组合是“**有**”的关系(狗有尾巴)——把一个类的对象当属性,比继承更灵活,能用组合就少用继承。**

- 组合:在 `__init__` 里把另一个类的对象赋给属性,如 `self.tail = Tail()`
- 依赖:某个方法**临时用到**另一个类的对象(作为参数传进来),用完即走,关系最松
- 继承层级过深难维护,组合可以随时拆装,课程建议:能用组合就不用继承
- 经典例子:学生有课程、老师有课程 → Course 类被 Student/Teacher 组合复用

```python
class Course:
    def __init__(self, name):
        self.name = name

class Student:
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses   # 组合:对象当属性

c = Course("Python基础")
s = Student("alex", [c])
print(s.courses[0].name)   # Python基础
```

### 4. 绑定方法与 classmethod / staticmethod
> 🎬 对应视频:P381~P382

**普通方法**绑定给对象**(第一个参数 self);`@classmethod` **绑定给类**(第一个参数 cls);`@staticmethod` **谁都不绑定**,就是放在类里的普通函数。**

- 对象绑定方法:通过对象调用时,解释器自动把对象传给 self
- 类方法:通过类或对象调用都自动把**类**传给 cls,可以访问/修改类属性
- 类方法常用来**替代构造方法**(工厂写法),如 `Date.from_string("2020-03-01")`
- 静态方法没有自动传入的 self/cls,适合与类相关但不需要对象和类状态的工具函数
- 普通函数写进类里就是对象绑定方法,加装饰器才能变成类方法/静态方法

```python
class Date:
    def __init__(self, y, m, d):
        self.y, self.m, self.d = y, m, d

    @classmethod
    def from_string(cls, s):
        y, m, d = map(int, s.split("-"))
        return cls(y, m, d)   # cls 就是类,用来造对象

    @staticmethod
    def is_valid(s):
        return len(s.split("-")) == 3

d = Date.from_string("2020-03-01")
print(d.y, d.m, d.d, Date.is_valid("2020-3-1"))   # 2020 3 1 True
```

### 5. property 装饰器与常用特殊方法
> 🎬 对应视频:P368~P369

**`@property` 把方法**伪装成属性**访问,配 setter 做受控读写;`__str__` 控制 print 显示,`__call__` 让对象能像函数一样加括号调用。**

- `@property` 让 `obj.score`(不带括号)像属性一样取值;`@score.setter` 拦截 `obj.score = 5` 做校验
- 好处:调用方写法不变,内部随时加校验逻辑
- `__str__`:print(对象) 时调用,**必须 return 字符串**;没有 __str__ 时退而调用 __repr__
- `__repr__`:交互式直接敲对象名、放在容器里打印时显示;调试常用
- `__call__` 让 `对象()` 可执行;`__eq__` 定义 == 行为;`__len__/__getitem__` 支持 len() 和下标

```python
class Score:
    @property
    def value(self):
        return self._v

    @value.setter
    def value(self, v):
        if not 0 <= v <= 100:
            raise ValueError("0-100之间")
        self._v = v

s = Score()
s.value = 95      # 触发 setter
print(s.value)    # 95,触发 getter
# s.value = 200   # ValueError
```

### 6. 反射、isinstance 与元类简介
> 🎬 对应视频:P383、P406~P407、P410

**反射四件套 **getattr / setattr / hasattr / delattr** 用**字符串**操作对象属性;`isinstance` 判实例、`issubclass` 判子类;type 既是查看类型的函数,也是所有类的**元类**。**

- `getattr(obj, "name", 默认值)` 取属性、`hasattr` 判存在、`setattr` 新增/修改、`delattr` 删除
- 典型用途:根据用户输入的**字符串**动态调用方法(框架路由的思路)
- `isinstance(obj, 类)` 判断对象是否是该类(或其子类)的实例;`issubclass(A, B)` 判断类的继承关系
- `type(对象)` 查看类型;`type("A", (object,), {})` 三参数形式可以**动态创建类**
- 元类 metaclass:class 语句创建类的过程实际由 type 完成,自定义元类可拦截类的创建(了解即可)

```python
class A:
    pass

a = A()
setattr(a, "age", 18)
print(getattr(a, "age"))    # 18
print(hasattr(a, "name"))   # False
print(isinstance(a, A), issubclass(A, object))   # True True
print(type(A))   # <class 'type'>
```

### 7. 隐藏属性(__x 与名称变形)
> 🎬 对应视频:P364~P365

**属性名以**双下划线开头(__x)即被隐藏**:类外取不到,解释器偷偷把它改名为 **_类名__x** —— 这是"变形"不是加密,目的是逼外部走接口。**

- __money 在类体内定义后,类外 obj.__money 报 AttributeError,但 obj._Person__money 仍能访问 —— 说明只是**名称变形**,并非真正私有
- 变形只发生在**类体内**定义的名字:类外部自己赋值的 obj.__x 不会变形,只是普通属性
- 为什么要隐藏:余额、密码这类数据不能让使用者随意改;隐藏后只暴露有限的接口方法,在方法内部做校验("存钱必须为正数"),控制权收回类手里
- 函数同样可以隐藏:def __run(self),思想一致 —— 对外接口越少越稳定
- 单下划线 _x 只是**约定**"别在外部用",Python 不做任何拦截;双下划线才触发变形

```python
class Person:
    def __init__(self, name):
        self.__money = 100    # 隐藏属性

    def get_money(self):      # 对外的接口
        return self.__money

p = Person("alex")
print(p.get_money())          # 100
# print(p.__money)            # ❌ AttributeError
print(p._Person__money)       # 100 变形后仍能访问(别这么用)
```

*隐藏属性与接口*

### 8. Mixins 多继承机制
> 🎬 对应视频:P376

**Mixin 是多继承的"守规矩"用法:**主功能放主父类,附加功能拆成一个个 Mixin 类**(命名 Mixin/able 结尾),按需自由组合。**

- 多继承的问题:父类一多,结构容易乱;Mixins 约定让多继承有秩序 —— 继承列表里只有**一个主父类**,其余都是功能插件
- 规范:Mixin 类**功能单一、不单独实例化**,类名以 Mixin / Flyable / Runnable 等结尾,一眼看出它是"功能包"而不是"物种"
- 经典示例:主干 Animal 提供 __init__、eat;FlyMixin 提供 fly;鸭子类 class Duck(Animal, FlyMixin) —— 鸭子是动物(主),会飞(功能)
- 查找顺序按 MRO 从左到右:属性先 Animal 再 Mixin,主父类写在前;Mixin 里只放增量功能,别和主父类重名互相干扰
- 标准库大量使用:socketserver 的 ThreadingMixIn 给服务器加多线程能力,django 的视图 Mixin 也是同一思路

```python
class Animal:
    def __init__(self, name):
        self.name = name

class FlyMixin:
    def fly(self):
        print("飞起来了")

class Duck(Animal, FlyMixin):   # 主功能 + 功能插件
    pass

d = Duck("鸭子")
print(d.name)   # 鸭子
d.fly()         # 飞起来了
```

*Mixins 组合功能*

### 9. 属性查找顺序(对象 → 类 → 父类)
> 🎬 对应视频:P372、P374、P377

**`obj.x` 的查找路线:**对象自身 → 类 → 按 MRO 依次找父类 → object**,全链找不到才抛 AttributeError;方法同样走这条链。**

- 第一步查**对象自己的名称空间**(__init__ 里 self.x = ... 创建的实例属性);没有才去类里找
- 类里也没有 → 沿 **MRO**(类.__mro__ 可查看)从左到右搜父类,终点是 object;全程未命中才报错
- 方法查找同理:子类重写后,对象调用的永远是**离它最近**的版本 —— 这就是"重写生效"的原理
- 想跨过重写版本直接用父类功能:父类名.方法(self) 或 super().方法()(按 MRO 找下一个,推荐)
- 遮蔽现象:obj.x = 新值 是给对象新增实例属性,不改类属性;但此后查找先命中对象级,类属性被"挡住"

```python
class A:
    def who(self):
        return "A"

class B(A):
    def who(self):
        return "B"

b = B()
print(b.who())                    # B:对象→B 类命中
print(super(B, b).who())          # A:跳到父类版本
print([c.__name__ for c in B.__mro__])   # ['B', 'A', 'object']
```

*属性查找顺序*

### 10. __new__ 与单例模式
> 🎬 对应视频:P413

**`类名()` 先执行 **__new__(cls) 创建并返回对象**,再把它交给 **__init__ 初始化**;重写 __new__ 让类"永远只产出一个对象",就是**单例模式**。**

- 分工:__new__ 负责"造对象"(第一个参数 cls,类级别);__init__ 负责"初始化对象"(第一个参数 self);__new__ 必须返回实例,__init__ 才会被调用
- 默认流程看不到:object.__new__(cls) 造出实例 → __init__ 给它挂属性 → 返回给调用方
- 单例写法:类属性 __instance = None;__new__ 里第一次创建并保存,之后每次都返回同一个实例 —— a = Singleton();b = Singleton();a is b → True
- 用途:全局只需一份的对象 —— 配置管理器、数据库连接池、日志对象;避免重复创建浪费资源、避免多处状态不一致
- 面试常问:__new__ 和 __init__ 的区别 —— 一个造实例(先),一个初始化实例(后);只重写 __init__ 拦不住"创建"这个动作

```python
class Singleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)   # 第一次才创建
        return cls.__instance                      # 永远返回同一个

a = Singleton()
b = Singleton()
print(a is b)   # True
```

*单例模式*

### 11. 内置方法补充(__getitem__ 系列、__del__)
> 🎬 对应视频:P409

**让对象支持 obj[key] 要实现 **__getitem__ / __setitem__ / __delitem__**;对象被回收时触发 **__del__**;双下方法都是"特定语法自动触发"的钩子。**

- __getitem__(self, key):让 obj[key] 可用;__setitem__ 支持 obj[key] = v;__delitem__ 支持 del obj[key] —— 自定义容器类三件套
- __getitem__ 里拿到切片会是 **slice 对象**:isinstance(key, slice) 判断后按 key.start/stop 处理,就能支持 obj[1:3]
- __del__ 析构方法:对象内存被回收时自动调用,一般用来收尾(关文件、断连接);但触发时机不完全可控,别把关键逻辑依赖它
- __hash__:返回对象哈希值,和 __eq__ 配对自定义"怎么算相等";放进 set/dict 做键的前提是可哈希
- 记忆口诀:双下方法不用手动调 —— print 触发 __str__、加括号触发 __call__、方括号触发 __getitem__、with 触发 __enter__/__exit__

```python
class Box:
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data.get(key)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        self.data.pop(key, None)

b = Box()
b["a"] = 1        # 触发 __setitem__
print(b["a"])     # 1 触发 __getitem__
del b["a"]        # 触发 __delitem__
print(b["a"])     # None
```

*下标三件套*

### 12. 菱形问题、MRO 与深度优先/广度优先
> 🎬 对应视频:P373、P375

**B、C 都继承 A,D 又同时继承 B、C,同名方法该用谁的?这就是**菱形问题**;py3 新式类用 **C3 线性化(MRO)** 解决,效果近似广度优先;py2 经典类深度优先会先撞上 A。**

- 菱形结构:class D(B, C),B、C 都继承 A —— D 调用 who() 时,公共父类 A 出现在两条查找路径上,顺序必须定死
- py3 一律新式类(继承 object),MRO 用 **C3 线性化**计算,类名.mro() 或 类名.__mro__ 可查看完整查找链
- 新式类菱形查找近似**广度优先**:D → B → C → A → object;B、C 的重写版本都优先于公共父类 A,写在继承列表前面的先找
- py2 经典类按**深度优先**:D → B → A → C,A 先于 C 被找到,可能挡住 C 里的重写版本 —— 这正是 py3 改用 C3 的原因
- super() 的真实含义不是"找父类",而是"沿 MRO 找下一个类";多继承里 super 链严格按 __mro__ 顺序走

```python
class A:
    def who(self):
        return "A"

class B(A):
    def who(self):
        return "B"

class C(A):
    def who(self):
        return "C"

class D(B, C):
    pass

print(D().who())                            # B:B 在前
print([c.__name__ for c in D.__mro__])      # ['D', 'B', 'C', 'A', 'object']
```

*菱形继承的查找顺序*

### 13. __call__ 方法与元类控制类的产生
> 🎬 对应视频:P411~P412、P414~P415

**对象加括号调用触发**类里的 __call__**;类加括号实例化触发**元类 type 的 __call__**——它先调类的 __new__ 造对象、再调 __init__ 初始化;在自定义元类里改写 __call__ 就能拦截实例化(单例的终极写法)。**

- 实例可调用:类里定义 __call__(self, *args) 后,obj(3) 就像调函数一样执行它;callable(obj) 可检测对象是否可调用
- 类的本质:type 是所有类的元类,类是 type 的对象;所以 类名() 触发 type.__call__,它内部依次调用该类的 __new__(cls) 和 __init__(self)
- 定制元类:class Meta(type) 重写 __call__(cls, *args, **kwargs) 拦截"实例化",在里面判断有没有已有实例就实现了单例;重写 __new__(mcls, name, bases, attrs) 则拦截"类的创建",可校验/修改类属性
- class Foo(metaclass=Meta) 指定元类;完整链路:类() → 元类 __call__ → 类 __new__ → 类 __init__,元类的 __call__ 先于 Foo 的 __new__/__init__ 执行
- 记忆口诀:对象() 找类的 __call__;类() 找元类的 __call__。日常业务很少手写元类,读框架源码(如 ORM 的 Model)时才会遇到

```python
class Meta(type):
    def __call__(cls, *args, **kwargs):
        print(f"拦截 {cls.__name__} 的实例化")
        return super().__call__(*args, **kwargs)   # 交给 type 继续:__new__ -> __init__

class Foo(metaclass=Meta):
    pass

f = Foo()              # 先打印拦截信息,再正常创建对象

class CallObj:
    def __call__(self, x):   # 对象可调用
        return x * 2

print(CallObj()(3))    # 6
```

*元类拦截实例化*

---

**系列目录 / 工具获取方式见文末 👇**