ʹ�÷�����

�������µ�index.html��ԭ���ģ���һ����ȫ��ͬ����
<div id="navi">
{% if show_prev %}<a href="/page/{{ pageindex|add:"-1" }}" >&laquo;��һҳ</a>{% endif %}
{% if show_next %}<a href="/page/{{ pageindex|add:"1"}}" >��һҳ&raquo;</a>{% endif %} 
</div>
����Ϊ��
{%mf pagenavi%}
{{ pageindex }},{{ pagecount }}
{%endmf%}