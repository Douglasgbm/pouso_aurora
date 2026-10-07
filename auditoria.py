"""Auditoria externa, sem alterar o repositório revisado. Passe sua pasta como argumento."""
from pathlib import Path
import sys, io, contextlib, itertools, json, subprocess, importlib.util
repo=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(repo))
import mgpeb as g
from exemplos import montar,casos
out={'arvore_modificada': bool(subprocess.check_output(['git','-C',str(repo),'status','--porcelain'],text=True).strip()), 'commit':subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip(),'checagens':[]}
def check(name,ok,detail):
 out['checagens'].append({'nome':name,'aprovado':bool(ok),'evidencia':detail})
for c,s,e,a,d in itertools.product((False,True),repeat=5):
 m=montar('X','Médico',fuel=12 if c else 11,sensores=s,sistemas=e)
 assert (g.autorizar(m,[a,'livre' if d else 'ocupada'],g.CONFIG)=='')==all((c,s,e,a,d))
check('32 combinações de autorização',True,'Apenas todas as condições verdadeiras autorizam.')
for f in (11.999,12,15,15.001):
 m=montar('M','Médico',fuel=f)
 assert (g.autorizar(m,[True,'livre'],g.CONFIG)=='')==(f>=12)
 if f>=12: assert g.vem_antes(m,montar('E','Energia'),g.CONFIG)==(f<=15)
check('4 fronteiras de combustível',True,'11.999 bloqueado; 12 e 15 urgentes; 15.001 não urgente.')
for name,args in [('contêiner inválido',(None,[],[True,'livre'],g.CONFIG)),('linha de módulo inválida',([42],[],[True,'livre'],g.CONFIG)),('linha de evento inválida',([montar('E','Energia')],[42],[True,'livre'],g.CONFIG))]:
 try:
  with contextlib.redirect_stdout(io.StringIO()): result=g.simular(*args)
  check(name,result==[],repr(result))
 except Exception as err:check(name,False,type(err).__name__+': '+str(err))
s=g.simular([montar('E','Energia')],[[6,'sistemas',False,'E']],[True,'livre'],g.CONFIG)
check('falha própria após pouso',s[0][0][g.ESTADO]!='operacional',{'estado':s[0][0][g.ESTADO],'sistemas':s[0][0][g.SISTEMAS]})
s=g.simular([montar('E','Energia'),montar('H','Habitação')],[[11,'sistemas',False,'E']],[True,'livre'],g.CONFIG)
check('propagação da falha de Energia',s[0][1][g.ESTADO]!='operacional',[(m[g.ID],m[g.ESTADO],m[g.SISTEMAS]) for m in s[0]])
s=g.simular([montar('E','Energia')],[[3,'sensores',False,'E']],[True,'livre'],g.CONFIG)
check('ativação com falha ao fim da descida',s[0][0][g.ESTADO]!='operacional',{'estado':s[0][0][g.ESTADO],'sensores':s[0][0][g.SENSORES],'historico':s[2]})
s=g.simular([montar('E','Energia',acidente=True)],[[6,'sistemas',True,'E']],[True,'livre'],g.CONFIG)
check('acidente preservado',s[0][0][g.ESTADO]=='acidente' and s[7]==[],s[0][0][g.ESTADO])
s=g.simular([montar('E','Energia'),montar('H','Habitação')],[[2,'area','livre','']],[True,'livre'],g.CONFIG)
check('pousos sequenciais',s[5]==10 and s[7]==[0,1],{'tempo':s[5],'pousados':s[7]})
# Reproduz todas as permutações de 5 candidatos para verificar a ordenação.
mods=[montar('E','Energia'),montar('H','Habitação'),montar('G','Logística'),montar('M','Médico',fuel=13),montar('L','Laboratório',fuel=12)]
for perm in itertools.permutations(range(5)):
 order=list(perm);g.ordenar(order,mods,g.CONFIG);assert order==[4,3,0,1,2]
check('120 permutações de ordenação',True,'Resultado L, M, E, H, G para margens e tipos escolhidos.')
actual=subprocess.check_output([sys.executable,'-X','utf8',str(repo/'exemplos.py')])
b=(repo/'exemplos_saida.txt').read_bytes()
try:b.decode('utf8'); valid=True
except UnicodeDecodeError:valid=False
check('saída salva UTF-8 e atual',valid and b==actual,{'utf8':valid,'igual_execucao':b==actual,'cenarios_executados':actual.count(b'===')//2})
spec=importlib.util.spec_from_file_location('gerador',repo/'gerar_relatorio_pdf.py');gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
u='https://science.nasa.gov/mission/mars-2020-perseverance/rover-components/'
converted=gen.converter_inline(u)
check('URL integral no gerador',f'href="{u}"' in converted,converted)
print(json.dumps(out,ensure_ascii=False,indent=2))

if not all(c['aprovado'] for c in out['checagens']):
 sys.exit(1)
