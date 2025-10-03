
# CPM / PERT + Gantt (Streamlit)

Aplicação **Streamlit** para montar **Diagrama de Redes (PERT/CPM)**, **Gráfico de Gantt** e a **tabela CPM (ES, EF, LS, LF, Folga)** a partir da lista de atividades do projeto.

> **Diferencial:** a duração da **Atividade O** é calculada automaticamente pelo **RU** do aluno (último dígito + 10). Ex.: RU `5020930` → `0 + 10 = 10` dias.

---

## 🧱 Estrutura do projeto

```
.
├── app.py                # App Streamlit
├── activities.csv        # Base de atividades (pode editar via interface)
└── requirements.txt      # Dependências
```

---

## ⚙️ Pré‑requisitos

- Python 3.9+
- Pip atualizado: `python -m pip install --upgrade pip`
- (Opcional) VS Code com extensão **Python**

---

## 🚀 Como executar

### Windows (PowerShell ou Terminal Integrado do VS Code)
```powershell
# 1) criar e ativar o ambiente virtual
python -m venv .venv
# se necessário (apenas na sessão atual):
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1

# 2) instalar dependências
pip install -r requirements.txt

# 3) rodar o app
streamlit run app.py
```

### Windows (Prompt de Comando - cmd)
```bat
python -m venv .venv
.venv\Scriptsctivate.bat
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Abra o link que o Streamlit mostrar (geralmente `http://localhost:8501`).

---

## 🖱️ Como usar

1. **Digite seu RU** na barra lateral → o app calcula automaticamente a **duração de O = (último dígito do RU) + 10**.
2. **Confira/edite a tabela** de atividades se necessário (a Atividade O é ajustada pelo RU).
3. Veja os **KPIs**: *Duração total do projeto* e *Caminho crítico*.
4. Consulte a **Tabela CPM** (ES, EF, LS, LF, Folga; atividades críticas marcadas).
5. Visualize o **Gráfico de Gantt** e o **Diagrama de Redes (precedência)**.
6. Use o botão **“Baixar modelo CSV”** para exportar/importar as atividades.

---

## 🗂️ Formato do `activities.csv`

| Coluna        | Descrição                                                                                      |
|---------------|-------------------------------------------------------------------------------------------------|
| `Activity`    | Identificador da atividade (ex.: A, B, C…).                                                     |
| `Duration`    | Duração em dias (inteiro).                                                                      |
| `Predecessors`| Lista separada por vírgulas com atividades predecessoras. Use **`-`** quando **não** houver.   |

**Exemplo mínimo:**
```csv
Activity,Duration,Predecessors
A,12,-
B,4,A
C,9,"B"
D,5,"B"
E,3,"B"
F,5,"C, D"
G,6,"E"
H,5,"E"
I,7,-
J,4,"I"
K,5,"J"
L,7,"J"
M,7,"L"
N,5,"L"
O,10,"F, G, H, K, M, N"
```

> Observação: quando houver múltiplos predecessores, eles devem estar **entre aspas** no CSV (como no exemplo).

---

## 📊 O que o app calcula

- **Caminho Crítico (CPM)** e **duração total** do projeto.  
- **ES/EF/LS/LF** e **Folga** por atividade.  
- **Gráfico de Gantt** com anotações `ES–EF` e marcação das atividades críticas (`*`).  
- **Diagrama de Redes** com setas de precedência, duração e ES/EF por nó (atividades críticas destacadas).

---

## 🧩 Como funciona (resumo)

1. **Ordenação topológica** pelas dependências.  
2. **Passo à frente (forward pass):** calcula **ES** e **EF**.  
3. **Passo para trás (backward pass):** calcula **LF** e **LS**.  
4. **Folga = LS − ES**. Atividades com **Folga = 0** são **críticas**.  
5. **Prazo do projeto =** maior **EF** observado (nó final).

---

## 🧪 Comandos úteis

```bash
# checar Python usado
python -V

# confirmar que o matplotlib está na venv
pip show matplotlib
pip list

# escolher o interpretador Python no VS Code
# (Ctrl+Shift+P -> "Python: Select Interpreter" -> escolha .venv)
```

---

## 🆘 Solução de problemas

- **“import matplotlib.pyplot could not be resolved (Pylance)”**  
  - Ative a venv e **instale as deps** (`pip install -r requirements.txt`).
  - Selecione a venv no VS Code (**Python: Select Interpreter**).  
  - Reinicie a janela do VS Code (**Reload Window**).

- **PowerShell bloqueando ativação da venv**  
  Use na mesma sessão:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .venv\Scripts\Activate.ps1
  ```

- **Porta ocupada**  
  ```bash
  streamlit run app.py --server.port 8502
  ```

---

## ☁️ Deploy (opcional)

- **Streamlit Community Cloud**  
  1. Suba os arquivos em um repositório Git.  
  2. No Streamlit Cloud, aponte para `app.py`.  
  3. Defina Python 3.9+ e inclua `requirements.txt`.

---

## 📄 Licença

Uso acadêmico/livre. Sinta-se à vontade para adaptar ao seu trabalho da disciplina.


By: Luis Gustavo Baido 