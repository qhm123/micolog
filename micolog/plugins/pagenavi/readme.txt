使用方法：

将主题下的index.html中原来的（不一定完全相同）：
<div id="navi">
{% if show_prev %}<a href="/page/{{ pageindex|add:"-1" }}" >&laquo;上一页</a>{% endif %}
{% if show_next %}<a href="/page/{{ pageindex|add:"1"}}" >下一页&raquo;</a>{% endif %} 
</div>
更改为：
{%mf pagenavi%}
{{ pageindex }},{{ pagecount }}
{%endmf%}