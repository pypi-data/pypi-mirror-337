from typing import List, Dict, Tuple
from autocoder.common.types import Mode, CodeGenerateResult
from autocoder.common import AutoCoderArgs
import byzerllm
from autocoder.common import sys_prompt
from autocoder.common.v2.code_auto_generate import CodeAutoGenerate
from autocoder.common import SourceCodeList

class CodeAutoGenerateStrictDiff(CodeAutoGenerate):
    """
    A class that handles code generation in strict diff format.
    """

    @byzerllm.prompt(llm=lambda self: self.llm)
    def single_round_instruction(
        self, instruction: str, content: str, context: str = "", package_context: str = ""
    ) -> str:
        """
        如果你需要生成代码，对于每个需要更改的文件，写出类似于 unified diff 的更改，就像`diff -U0`会产生的那样。
        下面是一些生成diff的要求：
        Make sure you include the first 2 lines with the file paths.
        Don't include timestamps with the file paths.

        Start each hunk of changes with a `@@ ... @@` line.
        Must include line numbers like `diff -U0` does.
        The user's patch tool need them.

        The user's patch tool needs CORRECT patches that apply cleanly against the current contents of the file!
        Think carefully and make sure you include and mark all lines that need to be removed or changed as `-` lines.
        Make sure you mark all new or modified lines with `+`.
        Don't leave out any lines or the diff patch won't apply correctly.

        Indentation matters in the diffs!

        To make a new file, show a diff from `--- /dev/null` to `+++ path/to/new/file.ext`.
        The code part of the diff content should not contains any line number.

        The path start with `---` or `+++` should be the absolute path of the file or relative path from the project root.

        下面我们来看一个例子：

        当前项目目录结构：
        1. 项目根目录： /tmp/projects/mathweb
        2. 项目子目录/文件列表(类似tree 命令输出)
        flask/
            app.py
            templates/
                index.html
            static/
                style.css

        用户需求： 请将下面的代码中的is_prime()函数替换为sympy。
        回答：
        好的，我会先罗列出需要的修改步骤，然后再列出diff。
        修改步骤：
        1. 添加sympy的import 语句。
        2. 删除is_prime()函数。
        3. 将现有对is_prime()的调用替换为sympy.isprime()。

        下面是这些变更的diff：

        ```diff
        --- /tmp/projects/mathweb/flask/app.py
        +++ /tmp/projects/mathweb/flask/app.py
        @@ ... @@
        -class MathWeb:
        +import sympy
        +
        +class MathWeb:
        @@ ... @@
        -def is_prime(x):
        -    if x < 2:
        -        return False
        -    for i in range(2, int(math.sqrt(x)) + 1):
        -        if x % i == 0:
        -            return False
        -    return True
        @@ ... @@
        -@app.route('/prime/<int:n>')
        -def nth_prime(n):
        -    count = 0
        -    num = 1
        -    while count < n:
        -        num += 1
        -        if is_prime(num):
        -            count += 1
        -    return str(num)
        +@app.route('/prime/<int:n>')
        +def nth_prime(n):
        +    count = 0
        +    num = 1
        +    while count < n:
        +        num += 1
        +        if sympy.isprime(num):
        +            count += 1
        +    return str(num)
        ```

        现在让我们开始一个新的任务:

        {%- if structure %}
        {{ structure }}
        {%- endif %}

        {%- if content %}
        下面是一些文件路径以及每个文件对应的源码：
        <files>
        {{ content }}
        </files>
        {%- endif %}

        {%- if package_context %}
        下面是上面文件的一些信息（包括最近的变更情况）：
        <package_context>
        {{ package_context }}
        </package_context>
        {%- endif %}

        {%- if context %}
        <extra_context>
        {{ context }}
        </extra_context>
        {%- endif %}

        下面是用户的需求：

        {{ instruction }}
        """
        
        if not self.args.include_project_structure:
            return {
                "structure": "",                
            }

        return {
            "structure": (
                self.action.pp.get_tree_like_directory_structure()
                if self.action
                else ""
            )
        }

    @byzerllm.prompt(llm=lambda self: self.llm)
    def multi_round_instruction(
        self, instruction: str, content: str, context: str = "", package_context: str = ""
    ) -> str:
        """
        如果你需要生成代码，对于每个需要更改的文件，写出类似于 unified diff 的更改，就像`diff -U0`会产生的那样。
        下面是一些生成diff的要求：
        Make sure you include the first 2 lines with the file paths.
        Don't include timestamps with the file paths.

        Start each hunk of changes with a `@@ ... @@` line.
        Must include line numbers like `diff -U0` does.
        The user's patch tool need them.

        The user's patch tool needs CORRECT patches that apply cleanly against the current contents of the file!
        Think carefully and make sure you include and mark all lines that need to be removed or changed as `-` lines.
        Make sure you mark all new or modified lines with `+`.
        Don't leave out any lines or the diff patch won't apply correctly.

        Indentation matters in the diffs!

        To make a new file, show a diff from `--- /dev/null` to `+++ path/to/new/file.ext`.

        下面我们来看一个例子：

        当前项目目录结构：
        1. 项目根目录： /tmp/projects/mathweb
        2. 项目子目录/文件列表(类似tree 命令输出)
        flask/
            app.py
            templates/
                index.html
            static/
                style.css

        用户需求： 请将下面的代码中的is_prime()函数替换为sympy。
        回答：
        好的，我会先罗列出需要的修改步骤，然后再列出diff。
        修改步骤：
        1. 添加sympy的import 语句。
        2. 删除is_prime()函数。
        3. 将现有对is_prime()的调用替换为sympy.isprime()。

        下面是这些变更的diff：

        ```diff
        --- /tmp/projects/mathweb/flask/app.py
        +++ /tmp/projects/mathweb/flask/app.py
        @@ ... @@
        -class MathWeb:
        +import sympy
        +
        +class MathWeb:
        @@ ... @@
        -def is_prime(x):
        -    if x < 2:
        -        return False
        -    for i in range(2, int(math.sqrt(x)) + 1):
        -        if x % i == 0:
        -            return False
        -    return True
        @@ ... @@
        -@app.route('/prime/<int:n>')
        -def nth_prime(n):
        -    count = 0
        -    num = 1
        -    while count < n:
        -        num += 1
        -        if is_prime(num):
        -            count += 1
        -    return str(num)
        +@app.route('/prime/<int:n>')
        +def nth_prime(n):
        +    count = 0
        +    num = 1
        +    while count < n:
        +        num += 1
        +        if sympy.isprime(num):
        +            count += 1
        +    return str(num)
        ```

        现在让我们开始一个新的任务:

        {%- if structure %}
        {{ structure }}
        {%- endif %}

        {%- if content %}
        下面是一些文件路径以及每个文件对应的源码：
        <files>
        {{ content }}
        </files>
        {%- endif %}

        {%- if package_context %}
        下面是上面文件的一些信息（包括最近的变更情况）：
        <package_context>
        {{ package_context }}
        </package_context>
        {%- endif %}

        {%- if context %}
        <extra_context>
        {{ context }}
        </extra_context>
        {%- endif %}

        下面是用户的需求：

        {{ instruction }}

        每次生成一个文件的diff，然后询问我是否继续，当我回复继续，继续生成下一个文件的diff。当没有后续任务时，请回复 "__完成__" 或者 "__EOF__"。
        """
        
        if not self.args.include_project_structure:
            return {
                "structure": "",                
            }

        return {
            "structure": (
                self.action.pp.get_tree_like_directory_structure()
                if self.action
                else ""
            )
        } 