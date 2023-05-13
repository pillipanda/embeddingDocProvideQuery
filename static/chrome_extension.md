---
alias: [chrome插件]
tags: [plugin, 插件, chrome]
date: 2023-04-27
---

```dataview
LIST join(file.tags, ", ")
WHERE contains(file.path, this.file.path)
```

Chrome 扩展的目录结构一般如下：
1.  根目录：扩展程序的根目录，包含以下文件和文件夹：
	-   manifest.json：必需的清单文件，描述扩展程序的基本信息、功能、权限等。
	-   background.js：后台脚本，可以监听和响应浏览器事件，例如用户打开新标签页、单击浏览器工具栏按钮等。
	-   popup.html：扩展程序弹出页面的HTML文件，当用户单击浏览器工具栏按钮时弹出。
	-   icon.png：扩展程序图标文件，包含16x16、32x32、48x48和128x128四种尺寸。
	-   locales：本地化文件夹，包含不同语言版本的翻译文件。
1.  options：包含扩展程序选项页面的HTML文件和JS文件，用户可以在此更改扩展程序的设置。
2.  content_scripts：包含注入到网页中的脚本和CSS文件，可以修改网页的样式和行为。
3.  images：包含扩展程序使用的图片文件。
4.  lib：包含扩展程序使用的第三方库文件。
5.  test：包含扩展程序的单元测试文件。

# manifest.json
manifest.json 是 Chrome 扩展程序的必需清单文件，它描述了扩展程序的基本信息、功能、权限等。它的内容结构如下：
1.  基本信息：
    -   manifest_version：必需的字段，指定清单文件的版本号，当前版本为2。
    -   name：扩展程序的名称，必需的字段。
    -   version：扩展程序的版本号，必需的字段。
    -   description：扩展程序的描述信息，可以包含HTML标签。
    -   icons：扩展程序的图标文件，包含16x16、32x32、48x48和128x128四种尺寸。
2.  权限：
    -   permissions：扩展程序需要的权限列表，可以包含多个权限。
    -   optional_permissions：扩展程序可选的权限列表，用户可以选择是否授予。
3.  **功能**：
    -   background：指定后台脚本的文件名，可以是JS或HTML文件。
    -   content_scripts：指定注入到网页中的脚本和CSS文件，可以修改网页的样式和行为。
    -   web_accessible_resources：指定扩展程序中可以访问的资源文件，例如图片、CSS文件、字体等。
4.  浏览器动作：
    -   browser_action：指定浏览器工具栏按钮的属性，包括图标、提示文字、弹出页面等。
    -   page_action：指定浏览器地址栏按钮的属性，与 browser_action 类似，但只在特定页面上显示。
5.  其他：
    -   manifest_key：扩展程序的公钥，用于验证扩展程序的身份。
    -   update_url：指定扩展程序的更新地址。
    -   content_security_policy：指定注入到网页中的脚本和CSS文件的安全策略。

需要注意的是，manifest.json 文件中的字段是有严格的格式和顺序要求的，不同版本的 Chrome 对清单文件的支持也有差异。因此，在编写 manifest.json 文件时，需要仔细阅读官方文档，并根据实际需要选择合适的字段和值。


# chatgpt-advanced
提交触发的函数：handleSubmit()

