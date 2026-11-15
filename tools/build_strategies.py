"""Собирает сайты стратегий из общего шаблона tools/strategy_template.html.
Запуск: python3 tools/build_strategies.py
Код страниц менять в шаблоне, параметры стратегий — здесь, затем пересобрать."""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL = (ROOT / 'tools' / 'strategy_template.html').read_text(encoding='utf-8')

STRATEGIES = {
  'kupony': dict(
    key='kup', title='Акции на купоны', start='2024-07-26',
    strat=[['Дата начала ведения стратегии', '26 июля 2024 г.'], ['Риск-профиль', 'Консервативный'], ['Срок', 'от 3-х лет'],
           ['Коротко о стратегии', '', 'Первоначальный капитал 1&nbsp;млн руб., 100% в облигациях. По мере получения купонов реинвестирование их в акции. Новые вложения на счёт (при наличии у вас) вкладывать в облигации.']],
    sheets=dict(gk='Портфель для гк', tx='Текущий портфель', ref='Справочник по облигациям'),
    txMode='lots', bench=dict(code='MCFTR', name='индекс Мосбиржи полной доходности'),
    compactRef=True,
    refNote='<b>Внимание!</b> В справочнике представлены все облигации, которые ранее были в портфеле. Чтобы увидеть актуальные — поставьте галочку «только бумаги в портфеле».'),
  'profit': dict(
    key='prf', title='Купонный профит', start='2024-06-11',
    strat=[['Дата начала ведения стратегии', '11 июня 2024 г.'], ['Риск-профиль', 'Консервативный'], ['Срок', 'от 1 года'],
           ['Коротко о стратегии', '', 'Всепогодный портфель из облигаций в условиях неопределённости ДКП. Первоначальный капитал разделён на 5 частей по 20%: LQDT (фонд денежного рынка), облигации с плавающим купоном, облигации с привязкой к валюте, ОФЗ и корпоративные облигации с постоянным купоном. В зависимости от стадии рынка и денежно-кредитной политики (ДКП) ЦБ пропорции будут меняться.']],
    sheets=dict(gk='Портф для гк', tx='Сделки по портфелю', ref='Справочник облигаций в портфеле'),
    txMode='deals', bench=dict(code='RGBITR', name='индекс государственных облигаций полной доходности')),
}

LINKS = {'switch': {'kupony': '<div class="switch"><div class="lnkrow"><span class="lbl">Стратегии</span><span class="lnk cur">Акции на купоны</span><a class="lnk" href="https://investprivet.ru/pl/teach/control/lesson/view?id=350821293&editMode=0" target="_top">Рост и доход</a><a class="lnk" href="https://investprivet.ru/pl/teach/control/lesson/view?id=350825211&editMode=0" target="_top">Купонный профит</a></div><div class="lnkrow"><a class="lnk risk" href="https://investprivet.ru/pl/teach/control/lesson/view?id=345529623&editMode=0" target="_top">🧭 Определить свой риск-профиль</a></div></div>', 'profit': '<div class="switch"><div class="lnkrow"><span class="lbl">Стратегии</span><a class="lnk" href="https://investprivet.ru/pl/teach/control/lesson/view?id=350825077&editMode=0" target="_top">Акции на купоны</a><a class="lnk" href="https://investprivet.ru/pl/teach/control/lesson/view?id=350821293&editMode=0" target="_top">Рост и доход</a><span class="lnk cur">Купонный профит</span></div><div class="lnkrow"><a class="lnk risk" href="https://investprivet.ru/pl/teach/control/lesson/view?id=345529623&editMode=0" target="_top">🧭 Определить свой риск-профиль</a></div></div>'}, 'learn_bond': '<div class="card learn" style="margin-top:14px"><h3>Полезные материалы</h3><div class="lnkrow"><span class="lbl">Обзоры</span><a class="lnk" href="https://investprivet.ru/pl/teach/control/lesson/view?id=349024524&editMode=0" target="_top">📊 Обзоры по облигациям</a></div><div class="lnkrow"><span class="lbl">Обучение по теме</span><a class="lnk" href="https://investprivet.ru/pl/teach/control/lesson/view?id=316068107&editMode=0" target="_top">🎓 Как оценить эмитента облигаций</a><a class="lnk" href="https://investprivet.ru/pl/teach/control/lesson/view?id=340640770&editMode=0" target="_top">🎓 Заявки на фондовом рынке</a><a class="lnk" href="https://investprivet.ru/pl/teach/control/lesson/view?id=343337766&editMode=0" target="_top">🎓 Расчёт доходности облигаций</a><a class="lnk" href="https://investprivet.ru/pl/teach/control/lesson/view?id=345525711&editMode=0" target="_top">🎓 Стратегии работы с облигациями</a><a class="lnk" href="https://investprivet.ru/pl/teach/control/lesson/view?id=349585962&editMode=0" target="_top">🎓 ВДО: как работать с облигациями</a></div></div>'}
for folder, cfg in STRATEGIES.items():
    cfg['switchHtml'] = LINKS['switch'][folder]
    cfg['learnHtml'] = LINKS['learn_bond']
    block = '/*CFG-START*/\nconst CFG = ' + json.dumps(cfg, ensure_ascii=False, indent=1) + ';\n/*CFG-END*/'
    html = re.sub(r'/\*CFG-START\*/.*?/\*CFG-END\*/', lambda m: block, TPL, flags=re.S)
    html = html.replace('/*TITLE*/', cfg['title'])
    out = ROOT / 'docs' / folder / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print('собран', out.relative_to(ROOT))
