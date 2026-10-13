import streamlit as st

import pandas as pd

import plotly.graph_objects as go

import plotly.express as px

from pathlib import Path

from html import escape



st.set_page_config(page_title='HerMetrics | Banking Intelligence', page_icon='📊', layout='wide', initial_sidebar_state='expanded')

ROOT = Path(__file__).resolve().parent

DATA = ROOT / 'data'

LOGOS = ROOT / 'assets' / 'logos'

BANKS = ['BIDV', 'MB', 'OCB', 'VCB', 'VietinBank']

BANK_COLORS = {'BIDV':'#D6A92C','MB':'#315BD4','OCB':'#9EBB38','VCB':'#138B6E','VietinBank':'#69A9D8'}

PILLARS = {'A':'Chiến lược & nguồn lực số','B':'Sản phẩm số & trải nghiệm khách hàng','C':'Công nghệ & dữ liệu','D':'Vận hành số & an toàn'}

PILLAR_COLORS = {'A':'#741B3B','B':'#B94C70','C':'#DC879E','D':'#E9B9C7'}

CRITERIA = [f'{p}{i}' for p in 'ABCD' for i in range(1,5)]



st.markdown('''<style>

:root{--wine:#681c38;--rose:#b85577;--ink:#263044;--line:#ece7eb}

.stApp{background:#f9f8fa;color:var(--ink)}

.block-container{max-width:1600px;padding:1.4rem 2rem 3rem}

[data-testid="stSidebar"]{background:linear-gradient(165deg,#fff 5%,#fff7fa 70%,#f5e8ef 100%);border-right:1px solid #eadfe5}

[data-testid="stSidebar"] .block-container{padding-top:1.5rem}

[data-testid="stSidebarNav"]{display:none!important}

[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{padding-top:1.0rem}

[data-testid="stSidebar"] .stPageLink a{padding:10px 13px;border-radius:10px;text-decoration:none;font-weight:600;font-size:14px}

[data-testid="stSidebar"] .stPageLink a:hover{background:#f6e7ee}

[data-testid="stSidebar"] .stPageLink a[aria-current="page"]{background:#f1dce6;color:#671a38}

[data-testid="stSidebar"] .stPageLink{margin-bottom:3px}

.hm-nav-title{font-size:10px;letter-spacing:2px;font-weight:750;color:#927887;margin:12px 0 10px}



[data-testid="stSidebarNav"] a:hover{background:#f4e3eb}

[data-testid="stSidebarNav"] a[aria-current="page"]{background:#f3dce5;color:#661a37}

h1,h2,h3{color:#321d2b!important;letter-spacing:-.5px}

.hm-brand{font-family:Georgia,serif;font-size:39px;letter-spacing:-1.8px;color:#741b3b;line-height:1.2;margin-bottom:3px}

.hm-brand-small{font-size:9px;letter-spacing:2.5px;color:#8a7280;margin-bottom:23px}

.hm-eyebrow{font-size:11px;letter-spacing:3px;font-weight:700;color:#667084;margin-bottom:10px}

.hm-title{font-family:Georgia,'Times New Roman',serif;font-size:clamp(32px,3.3vw,55px);font-weight:600;letter-spacing:-1.5px;line-height:1.08;color:#1e283a;margin-bottom:12px}

.hm-sub{font-size:14px;color:#697588;line-height:1.6;max-width:950px}

.hm-hero{padding:28px 28px 32px;position:relative;overflow:hidden;min-height:235px;border-radius:20px;background:linear-gradient(105deg,rgba(116,27,59,.94) 0%,rgba(151,53,91,.88) 35%,rgba(205,125,156,.65) 65%,rgba(248,230,238,.20) 100%),url("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCADcAeUDASIAAhEBAxEB/8QAHAAAAgIDAQEAAAAAAAAAAAAAAAECAwQFBgcI/8QASxAAAQQABAMEBggEAgYJBQAAAQACAxEEEiExBUFRBhMicTJhgZGhwQcUI0JSYrHRcqKy4SQzFUNjgpLwFhclNHODwtLxVGSVo7P/xAAZAQEBAQEBAQAAAAAAAAAAAAAAAQIDBAX/xAAiEQEBAQACAwEAAwEBAQAAAAAAARECIRIxQQMEUWEiM/D/2gAMAwEAAhEDEQA/APa0J0iltokUmhAklJJAkJoRSTQnSgVKBBbtt0KspFIK7d+H4ozH8PxU6RSKhmd+D4ot34PirMqMqgqt34PijX8PxVtIqk1cV6j7vxS1/D8VbSMqaKrP4fii3fh+KsypEUL2CaYrJcPufFALvwfFY/EeIDhpwjpYiYpXua8/eYA27A5+W6yw9k0bZI3gwuFtc03nHW+nxWfONeNRa+y4AAlppwDgaO9HoguP4PiuP4tLPgu0E+JwM3cTZWA6Wx4yDRzeY+I5FbnhPHoeJPbh5WfVsbX+S4219bljvvD1aEdEnLWuX52TW1JP4PijMfw/FWV1USFrXPEQ4/h+KeY/h+KdJgKauI5j+D4pgu/B8VMNTDU0whmP3PipeL8HxUgKT8lNXELd+D4ozO/B8VZXNJxAQVlzvwfFRs/g+KkTooE2rEIvP4fil3h/D8UJUtIO8/L8UZ/y/FFIQLOfw/FGf8vxT3RSqDP+U+9PP+U+9FIr1IDP+X4ozH8PxQGqWVTTCDj+H4p2fw/FMNUqTTELP4fii/y/FSRSCGY/h+KMx/D8VIhKkQsx/D8Usx/B8U0EqiJdX3figv8Ay/FBSVQ8/wCU+9Hefl+KSKRDz/l+KEkIMlBSlcyCIyyvZHGN3vcGge0rHw+OwuMBOFxUGIA37mVr69xKishCQcFJoLtgT5BAklZ3b/wO9yqkkjjnjgfIxk0gJZG5wDnAb0NzSgafNCEU0JoUUqTpCdIpUilKk6pTRFBTRSCNIpSpFKaIoUjWYNolxugB/wA0rGxAvp1EVdcrU1fSkW6VjA0U4E5idqrlz3VpiayW9zl3PmrHNvEMPRjv1CZb9qf4R+qntNcr2ym7iHBPIJAe+639Fcnge0UvCXtEZL4JJZM0R9HQXp0OvJdX24jL8NhABs55/lXm88bu7hAH+sl+S83PlnKvpfx+Ev5Tf/u3a8ZjH+lJn5T3ZykO6eAb9Frp2BvcnYieMg9PEt9xJoZjZP4Wf0NWgxzO77tzLrvmeD15ht0XXXPjNkbXh/aWXBgQ8QL58ONG4gC5GD84+8PWNeoO66qGRk8TJYntfG8ZmPaba4dQea86LDd3z9xWRwzE4nhQdNg3AXM4PikJMbxlaar7upOo1157Lc5OfP8AKfHoOVMNWHwrjWE4qCyO4sS0W/DyekPWOTh6x7aWyyrWuHrqqw1SAUsqKU1CyoqkydFEu0RSe7kFVak51qNWtQIklRpSpJVCpJSQqiKKUqQAiIgWnlUwEUmmIgJ0pVomB1TTCDU06tFUopUhNJVCQmkiEolMlJVLSKipEaKK0gQikIgQjmhAkJgIQeS/Rtw6D6QWcU492tzcWxMeJEEMOIJ7iIZA45WDQb16q9a1P0r9hMJ2VZg+0fZxjuHNMwhmZh3ubkeQS17CDbdiCLrZe18J4Vw/guDGD4ZgoMJhg4u7uFuUWdyep9a4T6csfDh+wkOEc4d7isbGGN50wFzj+g9qb2zZnFk/RR2txfa3s5O3iLxJxDASNillqu9a4Wxx9ehB8r5rQ/SvwbjHaXtbwbg3BTeIjwEuJeDP3QDTIG2T7FkfQNwqbC9nuJ8UlaWx4+drIb+82MEFw9WZxH+6Vfx/tjwXsx9K3EcdxfEOjbBwaHDQxxsL3yOdIXkAbbVuQl65dEtvGa8//wCqTt+DVw//AJJdr9GH0ece7OdqMRxXjjIA0YR0MJbiO9cXOc2/LQH3q2D6d+zE04Y/BcVijJrve7Y8DzDXWvQ+D8b4dx3ANx3CsZFi8M41njOx6OB1afUdUtqzjPjZEapUmDadLDoSE6RSKApBKlIBZAAhOkUopUilKkOsMJFX600QcWsbmcQB61Fxe4tyksF66a/2SewBpslziQLPn8FF7qo3QzBYvJuRe0tZXIX7yrWG3k+pYwfmLa0F7lXsrN7ElY5RZ/rR/Cf1R/rHeQ+aAR3h9QUtM7vILcc65jtaM31UeqQ/ALznFx02IV96T+oL0ntO+MT4YPIsxvDQTVk1svP8ZlidH3oI9M5QPEfH0Xh/a/8AdfZ/if8AjxdVxVxGOlvbw/0haTHhxij/APGj/rC3fE3VxHECRmVuag67Gw36LV4tmVkebbvo/wCoLu5cfUVmPPrs4aBw+fUKLbETmOoEYh9Vz8DNlkmlGENdFiGuAIOI2P8A4bVtisVxIkhIc9jhIMr2GnNOuoPIrqOGdqQxkMXFCGh0bD9bAptka5wPR15jTrS5p8LmzREDOzvReviG49v6q1mV0EJadDGArrPLjOXt6OHBwBaQQRYI5hIlcNgOJYrg0TRh2CXDd4c0DnVTavwH7pvlsfVuuwweMw+Pi7zDvuqzMcKcyxYsclXn5cPFcTag5SNhQViEUk0LQSSkikRFCmGp5U0VqQbopBqnWiaIBqMqnSKQRqklKkigEinSiTSqBIpWoklXGdSLlG1FSB1WkaqfEY7vuIOhnhDMJRbE+K847sOILrsc9eSnxHHyRcOjkwr4o8RiMohM5AaCRmN30APtpZMvDcNPJM+QzETEGSPvSGPoAC2jfQBXuw0L8Qyd7A57GuY0OFgA1enXQKssGbGSYjgZx+Ek7r7AzDMwP2aTlPt09iuknOB4XJi8TKJcjO8vKGXYFN95q/WrvqkAwcuFDS2GXPbQds12B0GpRNFFKyJkjczYnNcGnYkDS+vXzQY3DMU/FYL7Z8b8RE90Mxi9EvbzHqIIPtWUqYsPDDNNLE3IZcuYN0boKBA5GldugEIpOkAhCEEsTPBgsLLisVMyHDwsL5JHmmsaNSSV4h/oviP0zdsP9JvE2E7KYImGF7tHSNBtwYPxuO5+6KG4Wdx/t92Z7acWfw/inGH4HsxhZAXRRxSGXiThsSWtOSIdNzvppXUQfSr2BwWFjw2F4q2HDwtDI4o8FKGtaNgBlSazsrtcLhYMBhIcJhYmQ4eFgjijYKDGjQALBk7M8ExHFJuJz8Jwc+NmDQ+aaISOIaKFZrA0HJc/2W7cRdsu12Lg4QZDwjA4LNJI+LKZpnvGWgdQA1rulknoFrOw/wBK7+1fa9/Bp+Fx4WKVsjsK9khc8ZBdPvSyLOm1c1O2tjd9qfoz4B2k4XNHFw/C4PiGQnD4rDxCMtfyDsoAc0nQgrxj6KOLYrgf0g4TBOc5sOPecHiYr0za5T5hwq+hK+l8RiosHC/ETyNjhhaZJHuNBrRqSfYF83/RhwyftL9Jw4syJwwWDxEmOlfWjS4uMbPMk3XRpV43q6zyncx9I5aTTuwhc3Uk0UmooATpMBOlAk6RSkoI0h3olSUXEhunUJRTN4WA6XmCxzW511A1VuIPoD83yVDnVQ3ObYeRXOu3H0ua6g0+v91Y2SnkG7oaDdYjnEBguteXkVZG6nEDT/4QsZzHOMp0HoizfrKkNZH2bqvYqWSBr33qdNPYkHuMkmtagfBalcrx7aHtW5v1jDtdRHdPsHzC85xLy0RBj6Ijddi832h01Xa9sye+gLWl5ELiQN/S5fsuCkqQwuabaWOo1v4yvLzn/Vr6n8e5+XGO/wCJPDsfPprm+QWmx734eFrmkZO9j0y2R4x71uOIsriOINaZztuNFquIszYdpGo72Ov+Nq9GPPL6QZIH6aA3Q6H+/qKnhmkjFA7icf8A82qUkIzk7OOhNb+Y5owTzG/GZ2E/asNs107scjry21VwvI5YzTD/ALRv6qnurw0Bshwa4Bw8z71sJMkmGL2EOGhaW6g0Vl4Tg2JxMTWOjdHkLtxrua329vxVZvLPbSslcXCF7fGT4Q0Xm5afsspxfhsccRC98OIjY2MvGhbQ1BB0O+xXVYPguHwgbNl+1q8wOovlm391D1LiOOzDC9oOIyE2xkveOikP2Z8DdSOR9auMTn5V13DeOS8RYyEwNE7iW98P8s6GiBudeW3rVHAO08HGAzDzsGG4hlsxXbZK3MZ5+W49Y1Wu4BxjB4zicDI5QJhJlMT9HA8/P2Lj5GtutRldYLSQWkHQgjUH1ha49s3jN6evUilxHA+2LsPGIONSl8YkMYxpb6IABHeVy19IDTn1XcinNDmkFrhYINgjqEYsxGkw1Syp0gVI3UqRSiEAnSRNItUOtEiQOaRdoqTZ1KsiLbHVRLgEj4RqqybVkLUy/kFG7StC1IzoVE2IbDPhoi0k4h7mAg+jTC6z7qVxtY82GM+KwcoeAMPI55BHpWwt9m9qs1jycWijmx0RjfnwkRlrT7UBoc7L6xYBvqFZi8a7Duw8ccBlmxAJYwyCMGgCdTz1FDn7FHF8Gbi4Mc0zBkk7y+GQN1iJjDD5ggGx0KyOI4V+KgbCxuFkiqnx4mMvadNCKNgj58kTsnYwRjC95E9rsRII8pIthLS7XyykaKMvEH/WJocLg5MU+BodLlkayiRYaL3dWtabjVVf6Pc2Dh8XfukOEka4vfq6SmOb7/EqMXw2WR+JMDoC3FBveMna4gOAyhwynpWh6DUKjYT4yOF2Fa9pb9YcWguIbk8Bd4vdSpbiXYhuJ+rQ96+GbuQ3OAHmmmwdgPF8FQ/hjZIeHQyObLHhCMwlbm7yoyzX162snhuEbgHYgRtY2OWcytYxuUNGVoqv934odqeHYuXGw987CugYfQzSBxNEg6DbZZ1KrB4Q4TBxwlwcWXbgKu3E/NXUgEk0r1RQhCER5iPoC7OXrxbjH/FF/wCxWD6AuzXPivF/+KL/ANi9UpNTyp4RzPYzsJwvsPFjGcOnxU7sW5jnvxBaSMoNAZQNNSVqeL/RNwXHca/0zwvG47gvEe873vMG4Zc/Nwadr50QPUu9QQpt9r4xw3EOwXFeO4X6jx/tnxHGYAkZ8PhsLFhu9rk9zQSR6l0vA+AcN7O8NZw/hWEZhsM03lbqXO5ucTq4+srZpqa1JIKpCaKWVACdIpNQCEWi1FMJqOZGZEw7UXnQaEnNsEWk54BaNSTZoeX90q4x58wLRdaHQLHl8NVp4j+iyZiXS60AG7D1+v2LEm3b/E4/AKY6cajduZmcB4qF8zRoK0GnOA0139ipzBmQa5nO+RKk05i71lMXWZEftZj+Yf0hNjrdJ/GVjQyZ3TOYbaZSLrpTT8QVJj6zV+I/qsmOW7YzZOJ4cD/6e/5z+y8+ZMe9wjANMnT/AGhXcdsz/wBoQvzNNYdoc3mLe6iuGw8ZkxeAYDQcI81c7lK58pter8+WcI9Gx73fX8QSDRkNFa/GC4Cbq3sJ6GntW04hFkxeId/tHWDssGbhuJx8fdwjIXVlc/qHAg1udl1cdmHKzxG+quwXCMTNNOe7Ia8sc0kammkHTf2mlusDw1j8TK94yhjtNi42L8m78rPrXRQtY2PKxoAWp25cv08fTnMPwiGHCyzFhbI9pcXNNOPMWRt7Pet7G5rI8rQA2tAFBzQcAGjUmL5JEHLp0U9M2+XtdGQ+Jl7ZQvJ+3Mb28b4o5jrYQMzK3GRq9PiJEbNfuhec9sS08d4gx49OJpB9fdjT4Lc7OMysDs6A7tBD0bjmvHqJAF/FV46B2HxExGsQkf4vwjMfS/f3q7gBEePZoLOJjcT/AMC2XEIQziGKaOU0g/mKsdN7c/C6/rLDyk/WNq2/Du0OM4BO4Qjv8FoXYRxoN8Isxn7p3NbH1brWMwb24nHdwxuUZH5CSN2HY+zbbyUcQCJHA9ACOnhQsles8M4pg+L4fvsJJdVnjcKfGSLAcOX6Hks3KvJYJJcPicJisNM6DEDDxBsjN9qojYj1HRdtwHthh+Jtiw+N7vDY54AaAfs5T+UnY/lOvS1nHPlxs9OkqlBzq2SLrKSiCrTyoulW55PktYhvdyGyrvVIopakTQSSUqKkApZVUV0ilYRSWnRBXLLFh4XSzPDI21bjys1+pSgmgxLXOglbIGOyurdp6EHUFUcUjln4dLFCHGRzmVlq/TaSdegBPsVeHGIwn+kpJI5cTOX942TQd+A3wNAGgIrKR7earNZsWIhlfKyOVrnQvySAH0XUDR9dEe9QONwwjxEnfsyYdxZMfwEVofeFpeG4LiGAxre/EL2zxHvnw3/mg5szr65nDToFXi+HYp0OOlw0bjLPLJHJFt3kZeC1w9bdT6wSOiuI3008UUwikka15Y6SnGvC2rPkLCrGKhMUMokGSYgRuIIzE7V5rE41wzEcR4hA+BzWtZFJecWx5zxuax/PKcpuunsWTPFLi4MDL3Ekb/rMckkbqtgF3fl15qGrWSxvxJwwkaZwwPMd+INJIBrpYITGJwrcGMW6Zgw5AcJDsQdAsPEYCd3FZcbAAyaGOIwPdoHkF+eM+ogjyNHkqWwYmHg/CCcO502DLJJMPYzHwuBA5Fzc1jrSo2cGKw+La8wSh+R2V4LS0tO9EEAjRTNLX4KfHTYrFPxEcrICW9z3zGtfzzAhpOg0q9d1naqKEIGoTVCQmhBlIRSaw0EboQoBMJJgIoT2TDUV1WQJG0EqNop2laVotRTQlaaBqDzq3yJ/RO1TMTmFGhl5eaSCt7vtnXvQoexY0zjmGuniPxCsZ6UlfjP6BQLbOummnXUlaxdQLcz4TsA9x/kP7qUOrmUN38/NSIAljAGwcf6QpYcAZHHkbVS1Rwl94KNx1Lnucfa8q6F2eIHrZ+JWPwmhwnAuJpz4mvqtddfmnhHH6rCaItgOu65Y7f24/to2RvGCcru7+qRDNWl5nGrXHYOQxYvASvpsYEVFxHi+0Ow3K6btpipB2hc1s0rWjCxAta8gG824XBwvkxHFI3k6iZrG6bNaQAPcpjpLnGPUYOPtx3a8YGKD7MzytkdJuaa7YctQu7wuHYyFmRoGYAk8ya3J5ryHgEp/6zTA6NgzYrEOsA9Hr2GDwRx/wj9Fri4fr/jFwoDZJgNTY28llNkcDV6XsFi4WS3T2dMw/pCuDrfXrVYv+q4ZP8G0czHXwWVFToWHq0fosGFpETPKlkQyNjw8Ze4NGUDVC/4sYwdyw/lC817ZMvtFidNDCz+kr0OPFGWJvctptem8V7hv+i8/7a4h2F4+XSMEsTsJG52gDwbeLb18lriT320HB5S2drr2fG4+zIui4o4jjWOH/wBw/wDVcxw+SSNj+7iaHA5S+YaNocmbk7bke1b3jOIGH4zi+9NBzg8Sk+HxNB1/D57eS3i72rw9/XsWPxQxn+sKOIhjm7vMKcGtAe3cfuPUdFjDEFnEALIL4SPc4H5rKZ48PC+xqxul6qVuMEGQQYJ5acuRsYcBoSHEezZYeHcCIQ9oLc7CQRofEFvMBF3nB4QRvm/qctQcK6KFr4yCwZSWuOo1Gx+RVhbjq+z3aTF4bFtwGOLsTA6Z0cchP2kWpoH8TdPMetdrFiIcTAyfDyslieLa9hsH2rymSTueLu1HhxR21+8U8BxTF8LxbpsFJlLg3PE68kmrh4h10Go1U8f6YserEqO61PA+PYbjkIyAw4mjmw7yC7TctP3h6/eAtxlpGKjSKTRSqGNEWikUoFaKQnSqI0nSlSbPTb5hBWWG9tVDbVaB7DiOx8cQlczvJhH3jXatvEVYPqU2TYnGcU4dLOHRGGSTDSRg0HS924vNcxoK8yqmuga41dGuqlm0XL4nBz4rj2Obh42iVn1ctxJmIMOlmmjexy581k8anxL52Q4KHESyYYfWS2EWM1+BjtRoQH/BXE1vM9mtyjKXGq9i0/EJIMSOHPe8f6NneXPcTTXeG4w4/hJ66WAFnYKHh0uHlgw7YpcOZafG12ZgdpYHIDY0NLUNZJjLdwR7EqWBwOCCLhrJIo2Ne8vDnN3dT3VfktgUWEhCSBoUdUIM5CSFlo0BCYCgAFKkXSiXKCRdSgXWok2oo0kSklaRNNJ106BQMqnEYmLDR95K4hocGkgXVrI7txDcxLbcBQOq1/aAtiwcDRTQZbPsaVL6a45bI2EJbM1r2EFh2cDYPkudl4pi8JjMVJE/voe8ce5kOwBPou3G22o8lqoOITw8XwsWEmczvJGZ62ILq256Wg4oOziw5xzEtG4u+Sm9Os/PLddPguK4bHuEbHGOesxgloPrqBzHrFrKkb9qfICvYvOcdi4n28Rh7XM8LjoRQOo5g3zXoeEa5uGizkudkZZJsk5RutcXP9J4+lcZsOIblBc7nZ3SDfF7G/orI/8AK95+JTbduF/eoAeoUtuaotH1jLfibFdDcW7+yhLJ9XwU0g8OSJ79PU0ndXHSaUZayxto9bLisPjDhFwLiL7rLhZdT/AQoKuHv7vh2GbzbAyzzNMCIn1h461pg/RUDNHhyCaY2Kvc1SieBC0N1poF8tljHfXn/bR5/wCkWIsjSGFtf7l/NcpgaHEIiSGg4g6nzaui7bYhrO1mNaeQiAP/AJTVyeHd/i4Bd3ib/mar4p5+nZ9n35vpMicTY+t4kAVto9ewNfbGV+EfovEuzbyfpEw7uuNxP6SL2eJ7WRRmRwaC1u/PRMY5d3WPhTWc9SP6QspjgH2TsaPqWNhrMbqaWi93DU6ch+6NBPdl1O0vWvLorCrBKTG0R1V6uPTNyHPzUIwPC/Uvqsx1Ps6LEllIwhddaN1/3gsthGVoA1Gh9SYhQvLYWkmgAuK7ayNZxzDShnjdg2jN/vu0XZRi2Anelwn0gl0fE8C4bHCke55/ddOE7Y53pz2FlPfYwbgyuPvaFuOPykcUsggSQROBO2rB+y5nCykTTWat4v2tH7Lq+0ID5MASB48BEfi4fJdc7jHk5yJ/1fHRGNoczvCwNP3QW34Ty1G23kujwLo58HhnMcHU1oPUb7jkubLS3H4dpqjMHA/7jh8lscBOWYfDEaPbo13qs6HqPUsc+Pbr+fJvuGtA4dEOl/qVqJj/AIGTr3JP8tqzg/E2fUYGzkRuIGu7TZJq+R81SQXwOFHWMij/AA0sxvl6ZHEIGYjEvkYAyTNmsbO56/usJsEoldnjLTV1vpnfr8Qs8A00nZ0bDfmwK+GGOYODhoGWK0IOY6goS/GnLB3TXAua+J73Me0lrmurcEagrtOG9shG4Yfi3oZW5cW0dWg/aNHn6Q9oG65SbCPuUREOqRwo6GqvT3qsmzG4bGNh/lCuama9ajeyWNskb2PjcLa9hBBHUEbqdLSdj8v/AEZw7WigySVtDl4yfmt5SwwSKTpCBAJ0ndBRQBKjaaVqoAGhtZRW9Ug66kDe9krRuiFWpNCzvogAAkgAE7lNFKhZWhmTK3JVZaFV0pDWtY0NY1rWjYNFAexNIlEGgFAADoAlaEIBFJWi0UISQqM1OkrTtcwwEEpWokoplygSmVHVFO0jQFkgBLU6BKgH9SasqVYkCSHnLQa2wTuT5KxzAxgG7i5oJO51VWbw0TuR/wA/BSfLmfGAN33r6gSoLZD44x+Yn4FaDtPKM2FjP4Xu/QLekjvmXyaT+i5ftO/PxJjRsyAfEk/IKX01+c/6jT4Ah/aCBx+6WH3NJWHKQ5gLhel6+SyeGxkY+eU/ciefdHXzWJO/JAeoHLbZWR1t7YT2lzsPF1Y1vvK9VuiQBoHkdNtPkvMsARJ2j4bCW3csQOnIUfkvTBrBn6gu/UrUcf0u1VALgbdat25KyHVhdzL3f1FAywwtLnBrWgWSaAUIS50LcooGzZ33PJGQ8VJMTsQwfqsDjrzD2fx7mgZu5LQCL1JA1HtWwOVj5Tt6OZxPqWo7Tve3s9O6OMuzSRMBcCLuVuw3KE9sbES+CaySQ1ws+1MvJYa6KmVhdh5Hua5lt2e3LVmleSxjHV4z7h+6Olry3tnmPbDimpovaCDsaY3ktLw9jPrWGBDjIcQMtc9Wrou1OIgHaviolgY7/EFpcW2fRA6rRcGObimDbVl09f8A7GrXxl0HZcA/SDHlgawNxGIcXklxJyybXoPcvYoWsjALG+KhbibJ06leO9kXPl7axm/9biT/ACvXrrQ5zG2TsP0UxLVUM9MN6j1a8lLvC6bwjKM3MKqGOoduZVrQO8H8fzQt7YUrKwcjjvl+YWcw6+1Y8tDBSk7Bh/VXd41jzmNAmwNyfYh2lEfsxfKwuM+kKMul4Y8C7glF+T2/uura99ENYBTiLfqdzy2XL9uI5nwcMcxznyDv/S1v0DS1x9scp04IMqSWhVNYa/4guo48/wCy4S87HBln/DI4fNaJ0VOlMtYcmJvhlNE+I7dfYtzxgtmwHDHAPYA2VrXSNyh4zA9dN+dLrvcYytNMWOnwznDQTs16XY+alDKWQwgVQdW2u5UZGZHxB7dp4wQR+cBUl7oGvLWnNC5zmh2oOUk/JWzslyLsHIY44+gY0+6lfFjpMFLJHK100LHOGW/E0C/RPyPwVEkYjjdl2DCB5V/8KjHyEYydpbqXae0X81Ma8unSxSMlwsBa4EiCIPHNpyDcctEYcuM5IfTSxwy9fGNfZ81zzpS2SCSKQsf9Xip7Dr6AHt8itnwnG9/HhDPTZniQFwFNcS6vYdNlnOmt7baJmaeXb/Mb/SP2VUOFjdhItKcGloeN9CR7fJZcTHMlntutsOo9R/ZGGY5zHsI9CR7dB67+ay06bscC3hM8JIJjxDjp0IBXRUud7J5mux0RFasf7wR8l0hWL7RCkiFK0nEBpcSA0bkmgFBEqJcFhv4pAS9sAdOWtzW2gzevSPytYr8RiZSCZREAbyxDU+bj8gFcGdPi8PhQDPK2O9gdz5AalYU/FyInPgwj3hpbo8hpcC4DQct+dLUNiEUs5A8ZlfmdzPiO5U55HN4fiyw04Quc0jkRr8lrOk+ukwhbjQ7LIGOYafHYL2+fJa3imOn4VxJrgDNhnsp8XMEc2nr6jofUuVh4rJ9dJcWgtePG0ZXOaa5jzW/7QEuigk3p5afd/ZTO+2sbvC4uDG4dmIw0gkifs4foRyPqVxXCcPnn4fU2GcG/bFsjD6Lxm5jrrodx8F1uA4lBxFju7tkrP8yF/pM/cesaK2YljMKVotJGQhK9UWgEIvRJUCEiLQgzkItIuWFFpWlaEAUk0kDsAb1qqnO8QI9Z+XzUn8vaqhZf5NHxJ/ZTGokdXM9RJ+FfNSB+3YPU536D5qAHjJo6UBeg6+1N3+fVkgNHxN/JRU81zOrUhoHq6rlOOSNPFsQHEggNYCdj4evtXWR6uefzAfALk+IO73ieIeR4RO5x8gf7Ji8OXbAwkp+rcRkY0mo3Nzu0bbnBunM81rJ32wte0tsb7j3j5gLNgc5nA5zXpSRj3lzlrcQ64XkHZpWpC3tl8Ac3F9qMBKIwwMLn02zsw/2XoRc/6rQZlGQDxb+4LzT6P4XntBJTnZGYaRxbel20A+epXqL2EtaK3ICWZ0lu3SMIJYX+Mh4ou5eQ5IYajDY6Ltd9hqd/2U81vYGDNRJJ5bdVGBhELCaur0FLLJNiBmlJcXuDgLdsCG8h7VrO00pZw7CtG78bCPcS7/0rasOjyds7jftWl7TOY6PhTCT4sbmHh3DYnlUntqZHOfGcxslzf6grLLgenVKTLkAoavjGuvP3K1rQ6hufWtNPMO0rHS9pOLSUS12LkojXY18lh9n8M88TwcxAEUc5L3uIAHjb18ls+LWeNY9/4sVKf5ysTgkLXY6N5aCRZGm3iUt6WTtuuxEWHHayOp3SSn6w4BkdMFtcfSJs+wL1pjajYTQ0C8m7D4cRdp4njWoZjRH+zK9VGY1rW2g0VYsVwZO5aHEDU777nkotdqMrbOY6nQblQww+yaroG6tv8R03O5UWsDF5zgMRmJoMcQBoBqstrQHPIAAvfqozt/weIsCsj7B1vdTNWTzVPZNy2+tfGdlyP0gseeGYHISB3krTXO2tNfBda280mmma79gWh7YNjPCMK59lrcWQabY1jd+yvH2zynTzMNOVoI1bGK9Qzn911eJqXgGBO9TzMOnqaVrHQt+sscImAZX8uhafmtmWuPZyI5zbMZoSL3j6exdf6cmkxcUghY1rmhjZGO8Q9EB4NA/up4yANxGIjHN72/EhPHSMbhJXPGWmk6DMFlYkCTHThpH+e6wRY3+Hmr9PjXSm8Mw9YWn3sCw8dIHYxxPMMP8AI1bWHBl/D8OTYJiA1Gh0NUVq+Jw5ceMpNd1HYB0Ph6JPa51pN/7vhCBvA39SszBOYzCsY+iLlaQNR6d6+9VQwudg8KSNoy0UOjyrsBw/FTQzCGBxijxD7lNNY3MGnVxob3zT4e63HD+JOw7Js4knjzxsALrcwU86Xv5Fbnh00OIGIlhcHMMoI0o6sFgjkdCtRg+EOjjeHkylzmuHd+FoLc33nDXfkD5ra4fCPwcE7oXiJz4n33Io2AaJcbcSOWw9S58v8deO/XQdnn5OJ4gcnQD4O/ut/Ni4IAO+kDSdm7k+Q3K8+i4picC4yzguAZlMsIAeW2L8OxOx0q9ea3eEkw2KiGJwkzZmuOsgdZvob1B9RWbOzptZuMue0/V4QwcnS6n/AIR+61eOdJPM/vpHPAcaDjoBvoNuaUhLJHt6OI+KrkJdKXHchp0/hCs4s6ng2kCQbZmPA9hBVrpiPRF+eyWG1ptblw/lTyWAqtrGe+8VNyzPzbdWtPzUXNEkUzK9KNzfeCpzR1iDQ+4w/wAtfJTw8R7xumhNWfWr8Te3HsYTOw/jia72gf2XccQAm4QyVtekx+vQj+65N7Aw4QgggNeywdNHUuni/wAR2a/8n4g/2Wb8ajnu9LHYljo3ZA4SDKL5C/i1Z7gTiYp4XujeLLJGGiNAf+eSow8TvrMjaaQ5gOvqJHzV2EaPqGEd5NPxaVpXS8OxUuLwrnzBgkY9zCWCg6qo1y32WUtbwc0MSz8zXfCvktkss0IRSagW6KTKjaBoStCDMSQhRAhCSAStCEUn+kB0GwUGN8b9OYHuH91aW+I+dKDdI3u9bnfHRQQaLDnficT8kC3TyeEaEAHrp/dWZQ0BoG2iUWuZx5vcfj/ZFOI5fE78RJXDy4hzhI4usOzOo8rsrspnZMFI7pG4/ArmzhGR4Z2UtL3ANzDkEWNdKws4LC0MyF81nqaZv6vSWrnjLwGvAIJ5/uF03EYWiLDMANeN3xA+S1U+Ha8eG+fJX4v1L6PcORxLiEoZtA1up2zO6+xehyxAlud2YXdbBct2Owwgjxz283sbp6rPzXUOOaUC9gs32x9Skc1oJ2DWEqMYJiYGihlGrh6uii86TEXYbXwQJACGttzhWg+fRQzpBjB3QJtxsnXzK0XaICbGcKYXaNkleTV1Udf+pb+CNzoI+8dWmzf3Wl4/Ew8QgjaAA2Bxoetw/ZG57amUxtyhpe+pWCmtHK/dsroHOM0YDGtBe3c5jv7k+58LQBtINPY5XQRgYiLNoe8bpud1pr481xr3S4ydz2Ndczzmb4TWYnyKjwiJjZjTrewHMK21J+SvkjDs72uBJJJbVHc8v2U+HRZcNK8elmf/AErOt+PbZ9jYMvHmOOn2E2/8C9KZG5wbQoaauXnHZOOKLtA0U0TdxKT+IjKNSvQnTPeRZoaaBajlzmVRDlbEwuIF7dTqVPDnJYqvtHf1FY+HA7sOqjrr7VaQ4NeSQ1gkdZJrmeaJVcz/APDTgndrwANzukyUuaHNFWLHM7JjK5r2taTq4Fx0HP2lEEeaGK3EtyN8I0Gw96oiHfaPzkk5jlbvQrotT2wJd2fjqm1jGakZt2PW2awRMrQan9StR2sikf2ddoGj61EbdppTh81Z8Z5TXE985ssNNaLc5pcPXR25bLY4eTN2bnDvu4uI2fXG8fJaZ7ZmOioN1kNO3sgLo4MHGOyuJkcSXfWY9b000H9ZXS45yXWhxbBLg5vWx36K4i+0uLwzh4Hy20jey0FZGF4Rj8XC7JAWRlpHeS+Bux1s7+y10eD7Ixv4keI4iWV73FrmsH2bAQ2tyMx26BOXKSnGXHO8NiH1WONrTl0yt3NG7A01U39mZ8TPG6SaOCow1zCM8li/ujbluQu2xHDsPguGmOBjY2hzBUQyCs4B9Z0PMlYoDYhlaA1vQCgs+dt2OnjMytbhOC4XBxMh7hsndgkPxAD3eLxeiPCN/wAyy8QbhNuc8iSL0jdeLlyG/IJzS/bEAUcjP0WFjDeDmB2BjOv8YUna+kziIwQS7Mb5a2pjEiQ5GsrMHNsnXUELWyOygUC4B4GmgVkGYzxEkAd42w3z6rWMawsXiGy4KQC7Md17isOLGzYFz8XhJTFOG2XN2fXJw2cPNY+R8Mj2t2Li0sOx3Hs81TmDsMW6hxZVO8uq1jNuuyg49BicU6LEVBM53hJ0ZISL0J2PqPsJWxc0hwsV4G7+1cPiWh0jmmi1zW2DsfCFs+GcbxGCZAya58P3Qb/tGU53ok7+R9hUxZXWYWN3exurwh4s8tQQr2MAAJt38Og95VGBxeFxvd4jDSCUNe2yTbmm9iDq1bB0YJN2dSsfWmFK0GVpoC2tGmvN3X9k2Np+YC3dTqfer5IxbRX3T8CP3SAAJAFfNIjk+IxvhxRLDlIne06Ag3f7LpeAxHEcJcHSSHK5zAM2gBHT2rWcYw5c6dwAtsrZL6aD91tuzDv8NNHQ0eHX7Bol9NNJozEwkijkcyztyP7qUALIXsH+rmd5Vmv5q/ERmPE+JoIZKQdN9SFCCMGTFtArxZq82j5haNbThZy4x7ToXM/QrbUtRgvDi4Xcnae8Lc0s0RpI7KRCKUESlSlSK0QRQhCDMStCSiBCSSBoHpAetImt02HxeSCWurib5qJFRNb1ofNTcPAa6ILfGBoABaio/eB5CyURtywD+G/mm8ANe7fwqbhTSD5IKMbGG8Pl/gDf0WiMdhrerwt5xH/upG2ZwGvmtUxuWRoIzGyaCiz0xMcPtIm/hiHxJK1eJzNBc0lp5ELe4uInEO11AAPTZa3EQ2KIAs7hWNRtuy7COHSvkcfFMdz0AW5zfauytJ21Wu4JH3fDY7okucbHn/ZbJo1J9alZqtzSWTZnWDpQ26K8tDGHKAAAdAqnUI3k8z80STgsdlFijqsqsjaWxsHQD9Fz3GKPG2yZgWtwzWEDey5x+S3bnlwpztOg2Wi4hG5/EJco0DIxewGjv3ReM7UySO+zDfC0vNgc/DzKcRDMRGXUPGDrz1Q6OmsGYkguPh06IZHTwQK1s9dNVdbxwjoc0Y05KyDC/wDZsrnOeAZC0NaaGwJNrZCIGJocAaaKNajRSbEXYSOFoDQ57iTWu9fJRv6v7L8PGGx7pGx0XQyVQ1N1zXZBjAakNuv0Gan28gtJw1wMxjLW/wCU8ZhoTqFvAACABQB2CvGuf6Ttjw2IxlaG0Xa7nc+xOrc951dndqdSNTt0VkLT3W3N36lXRYcnNf43fqrrOMOMHxaHVzv1KyMBA5+HhLjQyN0HkFlsw4B23d81HDEQ4aJkhyuDB4eeg6exS8jDhw7Gx3lFlztee5Ws7R8PfjeDSQxRl7zJGQ0fxa7rZSYnLTY2AXZObkPJV1ncC52Z2Zt2dtVnyXx/txGG7E4idzO/m7tocXjumWTpR8Roe4FdLBweHhsIhjsscRI/N4yTY5kUPYF0DtHtvofkqMWGiNzjQAYf1C1eVrMxqSwNw+IOuYteC5xtxGu5Oqn3oYBZ5bBQxDy7DzBrS0Fr999isY6tBc7cA0PJWRbU8diWOwkgNAAA2dfvtWtkkN+Fvv8A2V+IsYXEBjf9WdfaFgPc4vpxrXYLcjNpSuPeDM4D7MbCublj4h4+p4vwmu6u/JzSst0BcWEMJPd7gfncqMVh3DC4gOLWl0MgokE+iTsPJa+M32wpHZvY8KUbsrmuPJwPxVjoQ0OLiTRBoef91MRPe0iGOzXIZj/Zb1jGjxTSzHSgtIaZSWnr4lhmHMwtrkR+q6HF4UfWJSR4S88wR15c1h/U/GcvM3SsqWNXI13gdRLe7ZqP4RyTYHGJnQZ27fmv5rYDDuOHhcBY7tvnsqxh6juiHCR1+WVqf0KcI6WAyyQvfHKx2Zr2GiLG3rGm2y7HB9pWPxDocewRamp2egf4h93ffbyXMQwkukFVbAf1WaMOe+Lj/wA7KXKsdw5hd3bm0QQ4ggiiNEu6AI5n1fuuZ4dPNgYWdy+2DN9k/Vu9ez2LfYTicGNyAXHKf9W/n5Hn+q55Y0wuMxlzJW/ka4Dy/wDhXdmnjv52n71O+Cu4lFmc01uwj/n3rH4S0xcRbQ0c0fNX4fUuLQA4qdo0JdmHwKwg0txpyuIzx8vUf7rb8Ti/xDX/AIm6rXZP8RHpqPfqCPkk9C3DSEMhed2kX7DS353Wlhw73sexjSTZoAXXNboYfFy1fdwjqfG73bfFSrpGqJ5DmqPrMTnFkWad43bEM1eZ2Csdw6P679s5047qwJDYsHU1tzCuiaI552hoAJa6gK5V8lE1j9xjZTdRYdv5jnd7hp8UpeFxvw8olfLM8scAXu0Brk0aLYA0nmCmjimcUxmEHdBzZmgAt70EkCuvP2oWTisHUpaK8JLdvWhdOh05KRITpLKFzCJCjqrMqKQV5TuVZG3fzCdBSaKCB1t5pgeIn2I5pAqKUmrSOpAUC/Mduak/kPXagBVUixXjvHE1vrtYLIqeSBypZuJ1yjzVDG+K/WixiTG8RJp94qiSMSVW2qynR2SeptR7vKjTY4OPu8HCPy371a1xr2pMNRMb0aP0SAJAsrKAVQB3JUHHM0gDluVIAABR5Io1J1PsC1WJF8RkNbZR/KtvS1szLxMrhzcVGuPtU5tvHkf1CWWmvP5H/wBJV7I9TascwCJ9Aeg79Ea1yv1chg8khE4NhIGxJ/mK20kAA2VUcBcIwG3odB5lZtdIu4Xhyca4i6Mb694XRNh12VHDcDJE7vJGBjcpGu/uWwL2t9Ft+spK5c7t6VwYduQl2niP6pF7Ii6yDbiQAoulc4mysWR2dx6bJrM4/wBrZcU8gUcgq6b+6xSaiJGmpOnmiSw519dPJUyEgNo7h36hM1uWT0C4uBJ3PwU4ZMrj6qP8wWObIN360RAZZNNMv/qC3iWt46TPK3SqtU44F0DgNyx1fAp1leCNrKlOLb7Cjm1rmB8T/W0/osJjCYmHbwDfyWdG+4gOrfkqImD6vEXkNtjdDudOi2jFlaPq8163E8fBY7ow0aUPJbGRjSxwDS62u3NDY+1YHektBAyChowa+/dWJWNiGvBjvwsyHV7g0ekevmsdzW93L4nOuN9923kQRufPosyRgc5j61yuFnffqlkGWQaWWO/Ra+J9YDCwRkMgBttXK4v+GgVZkleGiR7nAUcuw9w0WRu1lN5DUhQY0uH7ClpkYpro8S1zdC6NoOmhqxqOeyraGukFtyknlqP3C2E8YLITWoa4E+Tv7qjuQTqAUiMWOIdzGK2aR7nFWxYVpEmZtjM0/Aj5LJY3/DsBGanOAs67nmroowJDl1zMBo76E+/dTVYLcEGyGtiwjVTfCWuqiNNjX/PVbFjLmbY6j4KySBpkAIGoNJo1UMR7sg8nO/dWtgBaQRYDis+Lh8rnOAbVmxe+3RZcHCS4uzHTMbvTXyH7p5RcYsUs8kADnOlyOoA6uojkeazMHE4YiN4YbA1Fa79FnQ4GGIVV+rYe4fNZcGVrpWgACwaArl/ZYtFGIwr8SQ5zAwBpoE6n3furIeH4ZsbXFuckA67e5ZJI081BhLY2t6ClkSIDWFrQAK2ApSzqsu5palEKV1TRPon0mmvWP7KJJ+sFwFAsA19R/upEbeopEahUBJ6peakikGtxEP27zW5tCznsBdfqQrosQlY6hOx1CihNKx1CdjqEApjRRsdQjMOoUDvdHJRzDqEyR1RUXbpFIka6oBHUIqqQW72KIbQtWOrNuEiRW4UVjObQUctq9wB5pNZ4h5orIrdCEUoI9Ew1PZFjqEBSwnMuZ/8AEVm2OoUBG3NZI1UWVjsj1KtdA50T2tGpaQLWQ0MbtXmp5hzPxUXyYUfDWnWV3sb+6zIsPDBpFG1nrA196ecdQomQVuPepheVqb32AB61Q54Q54LhqOapLh1CuE6KSQ3Q003VRv2KdtzCyL81AkUdQNeZVxdQd6T/AD+QVUgvJ5H9VNxbndb7N7N8knBttOjd9z5KopqyRyI1VsbAGyfwH5J5o+Rs+5AfpILAtjtvJVNbKQhpFmteaT5fASB4g0kB2xVGZt7i+tqD3DXxD0SmIojDiwWQK5NFf3WPEQ2FgA+6NvJWtfWYEjcqDKy0K0A/RaQ2OJdR2WGGfZt05D9Fmtb4h5rHHoVporErFe0WwkH7w/RDGZn6DUgj4LIeywzUbn5KUYYJG9b5la1GqERIGhOnNSZFy21WSMuUbIY0HNQ5pqHLH9hCR+Jw+A/ZU92s8MD4mZhdPP6LHytG7vY0JpilrfBXR7ldEwh7HV4dQSUAtF0ALN3uU7G/r5lQXSGgCASQbHJZ2BAfEXPAzZiNNNFr84LacRa2WAc0xPFj0vkoM5tAUAAOgSaadIPzX8AoFwGxCTXDO7UbBBbaGGpCerQo5h1CBVjUIL7tA3KgHDqFIEXuFESQlY6hOx1CAOyRTsdQlYIqwgKQmmgg4WhTpCDLodEUOiaFEKh0RQ6ITQFDoih0QhQFDolQ6JoQKh0CKHRNCBUOgRQ6BNCBexVTQteMwADxrY5q5JFa+lNjM7g0c1EK7D/5vsKjd9MhsbGDwj2qVeoIQFXMUOgRXqCEICh0CVDoE0IpUOgRQ6BNCBUOgRQ6D3ITQKh0HuSyjoPcpIQRyjoPcnp0HuTSKA93uRQ6D3IRyQFDoPcih0CEIiOUdB7kUOg9yZQgVDoPcih0HuTQgVDoPcih0HuTSQAA6BP3IQgVDoPcih0HuQmgVDoPcih0HuQmgVDoPcmAOg9yipICh0HuRQ6BCEDodAih0HuQhAUOgRQ6BNCAodAih0CEICh0CC0EVQ9yEIMaWMMII2PwUFfP6A81QrFCEIVH/9k=") right center/auto 100% no-repeat;box-shadow:0 6px 24px rgba(88,40,60,.055);border:1px solid #f1e5eb;margin-bottom:18px}

.hm-hero .hm-title,.hm-hero .hm-sub,.hm-hero .hm-eyebrow{position:relative;z-index:1}

.hm-hero .hm-sub{max-width:610px;font-size:15px}

.hm-hero .hm-title{font-size:clamp(36px,3.5vw,56px)}



.hm-hero:after{display:none}

.hm-section{font-size:23px;font-weight:750;letter-spacing:-.4px;color:#2c2936;margin:28px 0 15px}

.hm-card{border:1px solid rgba(116,27,59,.09);border-radius:16px;padding:23px 22px;box-shadow:0 6px 18px rgba(45,26,39,.055);height:100%;transition:transform .2s ease,box-shadow .2s ease}
.hm-card:hover{transform:translateY(-3px);box-shadow:0 11px 24px rgba(45,26,39,.11)}
/* HerMetrics monochromatic ombre: burgundy -> dusty rose -> blush */
.hm-card.kpi-1{background:linear-gradient(125deg,#F2CEDD 0%,#FBEAF1 57%,#FFF9FC 100%)}
.hm-card.kpi-2{background:linear-gradient(125deg,#EAC1D2 0%,#F8E3EC 57%,#FFF7FA 100%)}
.hm-card.kpi-3{background:linear-gradient(125deg,#DFA8BF 0%,#F4D7E3 57%,#FFF4F8 100%)}
.hm-card.kpi-4{background:linear-gradient(125deg,#D9A1B9 0%,#F1CEDD 57%,#FFF1F7 100%)}
.hm-card.kpi-1 .hm-k-num,.hm-card.kpi-2 .hm-k-num,
.hm-card.kpi-3 .hm-k-num,.hm-card.kpi-4 .hm-k-num{color:#741B3B}
.hm-card .hm-k-label{color:#63384B;font-weight:650}
.hm-card .hm-k-note{color:#815B6C}
.hm-hero{border-color:#E9C9D6;box-shadow:0 8px 24px rgba(116,27,59,.09)}

.hm-k-label{font-size:12px;color:#7b7d8a;margin-top:4px}.hm-k-num{font-family:Georgia,serif;color:#741b3b;font-size:36px;line-height:1.2}.hm-k-note{font-size:11px;color:#9b96a1;margin-top:8px}

.hm-note{font-size:12px;color:#805569;background:#fcf1f6;border-left:3px solid #b95679;padding:11px 14px;border-radius:0 8px 8px 0;margin-top:13px}

.hm-heading{font-family:Georgia,serif;font-size:19px;font-weight:700;color:#2b2631;margin-bottom:8px}

.hm-table{width:100%;border-collapse:collapse;font-size:13px}.hm-table td,.hm-table th{padding:11px 6px;border-bottom:1px solid #f0edf0;text-align:left}.hm-table th{font-size:11px;color:#8b8791;font-weight:600}.hm-bar{height:12px;border-radius:6px;background:linear-gradient(90deg,#d48da5,#741b3b)}

[data-testid="stVerticalBlockBorderWrapper"]{background:#fff;border-color:#ebe6ea!important;border-radius:14px!important;box-shadow:0 4px 14px rgba(45,26,39,.035)}

[data-testid="stPlotlyChart"]{border:none!important;box-shadow:none!important;background:transparent!important;padding:0!important}

[data-testid="stDataFrame"]{border-radius:12px;overflow:hidden}

[data-testid="stMetric"]{background:white;border:1px solid #eee7ec;border-radius:12px;padding:13px}

.stButton>button,.stDownloadButton>button{background:#741b3b;color:white;border:0;border-radius:9px}

.stButton>button:hover,.stDownloadButton>button:hover{background:#9e3c60;color:white}


/* HerMetrics interactive navigation and controls — original hero retained */
[data-testid="stSidebar"] { min-width: 280px !important; width: 280px !important; }
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] { padding-left: 18px !important; padding-right: 18px !important; }
[data-testid="stSidebar"] .hm-brand { font-size: 35px !important; white-space: nowrap; letter-spacing: -1.6px; }
[data-testid="stSidebar"] .stPageLink { width: 100%; margin: 3px 0 !important; }
[data-testid="stSidebar"] .stPageLink a,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
  display: flex !important; align-items: center; gap: 9px;
  width: 100%; min-height: 43px; padding: 10px 13px !important;
  border-radius: 10px !important; border-left: 3px solid transparent;
  color: #475066 !important; font-size: 13px !important;
  font-weight: 600 !important; line-height: 1.35 !important;
  transition: background .18s ease, color .18s ease, border-color .18s ease, transform .18s ease;
}
[data-testid="stSidebar"] .stPageLink a:hover,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
  background: #f3dce6 !important; color: #681c38 !important;
  border-left-color: #b85577 !important; transform: translateX(2px);
}
[data-testid="stSidebar"] .stPageLink a[aria-current="page"],
[data-testid="stSidebar"] .stPageLink a[aria-current="true"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="true"],
[data-testid="stSidebar"] .stPageLink:has([aria-current="page"]) a,
[data-testid="stSidebar"] .stPageLink:has([aria-current="true"]) a {
  background: #741b3b !important; color: #fff !important;
  border-left-color: #e5b0c3 !important;
  box-shadow: 0 3px 10px rgba(116,27,59,.14);
}
[data-testid="stSidebar"] .stPageLink a[aria-current] *,
[data-testid="stSidebar"] .stPageLink:has([aria-current]) a * { color: inherit !important; }
/* Multiselect: replace bright red selected tags with muted rose */
span[data-baseweb="tag"] { background: #f3e2ea !important; color: #681c38 !important;
  border: 1px solid #e7cad6 !important; border-radius: 7px !important; }
span[data-baseweb="tag"] span, span[data-baseweb="tag"] svg { color: #681c38 !important; fill: #681c38 !important; }
[data-baseweb="select"] > div, [data-baseweb="input"] > div {
  background: #fff !important; border: 1px solid #e8dce3 !important;
  border-radius: 10px !important; min-height: 41px;
  transition: border-color .18s ease, box-shadow .18s ease;
}
[data-baseweb="select"] > div:hover, [data-baseweb="input"] > div:hover { border-color: #b85577 !important; }
[data-baseweb="select"] > div:focus-within, [data-baseweb="input"] > div:focus-within {
  border-color: #8e3154 !important; box-shadow: 0 0 0 3px rgba(184,85,119,.12) !important;
}
[data-testid="stTextInput"] input { color: #263044 !important; font-size: 14px !important; }
[data-testid="stTextInput"] input::placeholder { color: #9c95a0 !important; }
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: #584658 !important; font-weight: 650 !important; font-size: 12px !important; }
[data-testid="stSidebar"] [data-baseweb="select"] { margin-bottom: 3px; }
/* Improve button hover while leaving all charts and KPI styling untouched */
.stButton > button, .stDownloadButton > button { transition: background .18s ease, box-shadow .18s ease, transform .18s ease; }
.stButton > button:hover, .stDownloadButton > button:hover { box-shadow: 0 4px 12px rgba(116,27,59,.16); transform: translateY(-1px); }


/* Prominent website brand inside hero; readable on burgundy overlay */
.hm-hero .hm-site-name{position:relative;z-index:2;display:inline-block;font-family:Georgia,'Times New Roman',serif;font-size:25px;font-weight:700;letter-spacing:-.6px;color:#FFFFFF !important;margin-bottom:12px;text-shadow:0 2px 10px rgba(50,12,30,.35)}
.hm-hero .hm-title{max-width:650px}
/* HERO TITLE: ombre wine-to-rose overlay, keep building image */
.hm-hero .hm-title { color:#FFFFFF !important; text-shadow:0 2px 10px rgba(65,16,38,.16); }
.hm-hero .hm-eyebrow { color:#FCE5EF !important; }
.hm-hero .hm-sub { color:#FFF1F6 !important; }
.hm-hero { border-color:#DCA9BF !important; }

/* HerMetrics readability upgrade: typography only, preserve layout and colors */
html, body, [data-testid="stAppViewContainer"] {font-size:17px !important;}
.hm-hero .hm-site-name{font-size:31px !important;}
.hm-hero .hm-eyebrow{font-size:13px !important;letter-spacing:2.1px;}
.hm-hero .hm-title{font-size:clamp(40px,3.9vw,62px) !important;line-height:1.12;}
.hm-hero .hm-sub{font-size:17px !important;line-height:1.65;}
.hm-brand{font-size:42px !important;}
[data-testid="stSidebar"] .hm-brand{font-size:40px !important;}
.hm-brand-small{font-size:11px !important;}
.hm-nav-title{font-size:12px !important;}
[data-testid="stSidebar"] .stPageLink a{font-size:16px !important;}
.hm-section{font-size:27px !important;}
.hm-heading{font-size:22px !important;}
.hm-k-num{font-size:42px !important;}
.hm-k-label{font-size:15px !important;}
.hm-k-note{font-size:13px !important;line-height:1.5;}
.hm-note{font-size:14px !important;line-height:1.65;}
.hm-table{font-size:15px !important;}
.hm-table th{font-size:13px !important;}
.hm-table td,.hm-table th{padding:13px 8px !important;}
[data-testid="stTextInput"] input{font-size:16px !important;}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p{font-size:14px !important;}
[data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p{font-size:15px;line-height:1.6;}
[data-testid="stSelectbox"] *,[data-testid="stMultiSelect"] *,[data-testid="stRadio"] label{font-size:15px;}
[data-testid="stDataFrame"]{font-size:15px;}
@media(max-width:900px){.hm-hero .hm-title{font-size:clamp(32px,6vw,46px) !important}.hm-hero .hm-site-name{font-size:26px !important}.hm-k-num{font-size:35px !important}}
</style>''', unsafe_allow_html=True)



@st.cache_data

def load_evidence():

    path = DATA / 'Evidence_Final.xlsx'

    if not path.exists(): raise FileNotFoundError(f'Không tìm thấy {path}')

    d = pd.read_excel(path, sheet_name='Evidence_Raw', engine='openpyxl')

    d.columns = d.columns.astype(str).str.strip()

    required = ['bank','criterion','filename','page','context']

    missing = [c for c in required if c not in d.columns]

    if missing: raise ValueError(f'Thiếu cột: {missing}')

    d['bank'] = d['bank'].astype('string').str.strip().replace({'VTB':'VietinBank','Vietinbank':'VietinBank'})

    d['criterion'] = d['criterion'].astype('string').str.strip().str.upper()

    d['pillar'] = d['criterion'].str[0]

    d['pillar_name'] = d['pillar'].map(PILLARS)

    if 'criterion_name' not in d.columns: d['criterion_name'] = d['criterion']

    if 'filter_stage' not in d.columns: d['filter_stage'] = 'Không phân loại'

    d['filter_stage'] = d['filter_stage'].astype('string').fillna('Không phân loại').str.strip()

    return d



@st.cache_data

def load_ranking():

    path = DATA / 'ranking.csv'

    if not path.exists(): return None

    d = pd.read_csv(path, encoding='utf-8-sig')

    if not {'bank','rank','BDTI','A','B','C','D'}.issubset(d.columns): return None

    for c in ['rank','BDTI','A','B','C','D']:

        d[c] = pd.to_numeric(d[c],errors='coerce')

    return d.dropna(subset=['rank','BDTI']).sort_values(['rank','bank'])



try:

    evidence = load_evidence()

    ranking = load_ranking()

except Exception as e:

    st.error(f'Lỗi tải dữ liệu: {e}')

    st.stop()



with st.sidebar:

    st.markdown('<div class="hm-brand">HerMetrics</div><div class="hm-brand-small">BANKING INTELLIGENCE</div>',unsafe_allow_html=True)

    st.markdown('<div class="hm-nav-title">WORKSPACE</div>',unsafe_allow_html=True)

    st.page_link('app.py',label='Overview',icon=':material/dashboard:')

    st.page_link('pages/2_Ranking_Dashboard.py',label='Ranking',icon=':material/leaderboard:')

    st.page_link('pages/3_Bank_Profile.py',label='Bank Profile',icon=':material/account_balance:')

    st.page_link('pages/4_Bank_Comparison.py',label='Bank Comparison',icon=':material/compare_arrows:')

    st.page_link('pages/1_Evidence_Explorer.py',label='Evidence Explorer',icon=':material/search:')

    st.page_link('pages/5_Scoring_Evidence_Audit.py',label='Scoring Audit',icon=':material/fact_check:')

    st.page_link('pages/6_Data_Validation.py',label='Data Validation',icon=':material/verified:')

    st.markdown('---')

    st.markdown('<div class="hm-nav-title">EVIDENCE FILTERS</div>',unsafe_allow_html=True)

    banks_present = [b for b in BANKS if b in evidence['bank'].dropna().unique()]

    selected_banks = st.multiselect('Ngân hàng', banks_present, default=banks_present)

    selected_pillars = st.multiselect('Trụ cột', list(PILLARS), default=list(PILLARS),format_func=lambda p:f'{p} — {PILLARS[p]}')

    available_criteria = [c for c in CRITERIA if c[0] in selected_pillars and c in evidence['criterion'].dropna().unique()]

    selected_criteria = st.multiselect('Tiêu chí',available_criteria,default=available_criteria)

    stages = sorted(evidence['filter_stage'].dropna().unique().tolist())

    selected_stages = st.multiselect('Tầng bằng chứng',stages,default=stages)

    st.markdown('---')

    st.caption('HerMetrics · Vietnam Banking 2025')



filtered = evidence[

    evidence['bank'].isin(selected_banks)

    & evidence['pillar'].isin(selected_pillars)

    & evidence['criterion'].isin(selected_criteria)

    & evidence['filter_stage'].isin(selected_stages)

].copy()



st.markdown('''<div class="hm-hero"><div class="hm-site-name">HerMetrics</div><div class="hm-eyebrow">VIETNAM COMMERCIAL BANKS</div>

<div class="hm-title">Digital Transformation<br>Ranking 2025</div>

<div class="hm-sub">Nền tảng phân tích, so sánh và xếp hạng mức độ chuyển đổi số của 5 ngân hàng thương mại Việt Nam.</div></div>''',unsafe_allow_html=True)



# Dashboard KPIs, all calculated from filtered evidence

kpis = [

    ('Ngân hàng',str(filtered['bank'].nunique()),'Đang hiển thị'),

    ('Tiêu chí',str(filtered['criterion'].nunique()),'Trong bộ lọc hiện tại'),

    ('Dòng bằng chứng',f'{len(filtered):,}','Số dòng dữ liệu nguồn'),

    ('Nguồn báo cáo',str(filtered['filename'].nunique()),'Tệp tài liệu được ghi nhận')

]

cols = st.columns(4,gap='small')

for i,(col,(label,num,note)) in enumerate(zip(cols,kpis),start=1):

    with col:

        st.markdown(f'<div class="hm-card kpi-{i}"><div class="hm-k-num">{escape(num)}</div><div class="hm-k-label">{escape(label)}</div><div class="hm-k-note">{escape(note)}</div></div>',unsafe_allow_html=True)



st.markdown('<div class="hm-note">Các chỉ số trên phản ánh <b>số lượng bằng chứng sau khi lọc</b>, không phải điểm BDTI. BDTI là điểm ước tính từ quy trình chấm tự động, chưa được xác nhận độc lập.</div>',unsafe_allow_html=True)



st.markdown('<div class="hm-section">Banking Intelligence Overview</div>',unsafe_allow_html=True)

left, right = st.columns([1.28,1],gap='medium')

with left:

    with st.container(border=True):

        st.markdown('<div class="hm-heading">Overall Ranking 2025</div>',unsafe_allow_html=True)

        if ranking is None:

            st.info('Chưa có ranking.csv hợp lệ để hiển thị bảng xếp hạng.')

        else:

            rank_show = ranking[ranking['bank'].isin(selected_banks)].sort_values('rank')

            if rank_show.empty: st.info('Không có ngân hàng trong bộ lọc.')

            else:

                rows = []

                for _,r in rank_show.iterrows():

                    score = float(r['BDTI'])

                    width = max(0,min(100,score))

                    rows.append(f'<tr><td><b>#{int(r["rank"])}</b></td><td>{escape(str(r["bank"]))}</td><td style="width:44%"><div style="background:#f7edf1;border-radius:6px;height:12px"><div class="hm-bar" style="width:{width:.2f}%"></div></div></td><td><b>{score:.3f}</b></td></tr>')

                st.markdown('<table class="hm-table"><thead><tr><th>Hạng</th><th>Ngân hàng</th><th>BDTI</th><th>Điểm / 100</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>',unsafe_allow_html=True)

                st.caption('Nguồn: ranking.csv · Chỉ lọc ngân hàng; điểm BDTI không tính lại theo bộ lọc bằng chứng. Kết quả chấm tự động cần rà soát.')

with right:

    with st.container(border=True):

        st.markdown('<div class="hm-heading">Performance by Dimension</div>',unsafe_allow_html=True)

        if ranking is None or ranking.empty:

            st.info('Chưa có điểm trụ cột.')

        else:

            eligible = ranking[ranking['bank'].isin(selected_banks)]['bank'].tolist()

            if eligible:

                bank = st.selectbox('Ngân hàng phân tích',eligible,key='overview_radar_bank')

                r = ranking.loc[ranking['bank'].eq(bank)].iloc[0]

                vals = [float(r[p]) for p in PILLARS]

                fig = go.Figure(go.Scatterpolar(r=vals+[vals[0]],theta=list(PILLARS)+['A'],fill='toself',fillcolor='rgba(155,56,91,.16)',line=dict(color='#741b3b',width=3),marker=dict(size=7),name=bank))

                fig.update_layout(height=325,showlegend=False,margin=dict(l=35,r=35,t=18,b=10),paper_bgcolor='rgba(0,0,0,0)',font=dict(color='#586275'),polar=dict(bgcolor='rgba(0,0,0,0)',radialaxis=dict(range=[0,100],gridcolor='#eee6eb',tickvals=[25,50,75,100]),angularaxis=dict(gridcolor='#eee6eb')))

                st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})

            else: st.info('Hãy chọn ít nhất một ngân hàng.')



st.markdown('<div class="hm-section">Evidence Analytics</div>',unsafe_allow_html=True)

col_a,col_b = st.columns([1.15,1],gap='medium')

with col_a:

    with st.container(border=True):

        st.markdown('<div class="hm-heading">Evidence by Bank</div>',unsafe_allow_html=True)

        counts = filtered.groupby('bank').size().reindex(BANKS,fill_value=0)

        fig = go.Figure(go.Bar(x=counts.values,y=counts.index,orientation='h',marker_color=[BANK_COLORS[b] for b in BANKS],text=counts.values,textposition='outside'))

        fig.update_layout(height=330,showlegend=False,margin=dict(l=8,r=45,t=12,b=25),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',xaxis=dict(title='Số dòng bằng chứng',gridcolor='#f0edf0'),yaxis=dict(autorange='reversed',title=''))

        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})

with col_b:

    with st.container(border=True):

        st.markdown('<div class="hm-heading">Evidence by Pillar</div>',unsafe_allow_html=True)

        pc = filtered.groupby('pillar').size().reindex(list(PILLARS),fill_value=0)

        fig = go.Figure(go.Bar(x=pc.index,y=pc.values,marker_color=[PILLAR_COLORS[p] for p in pc.index],text=pc.values,textposition='outside'))

        fig.update_layout(height=330,showlegend=False,margin=dict(l=10,r=10,t=12,b=25),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',xaxis=dict(title='Trụ cột'),yaxis=dict(title='Số dòng bằng chứng',gridcolor='#f0edf0'))

        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})



st.markdown('<div class="hm-section">Evidence Matrix</div>',unsafe_allow_html=True)

with st.container(border=True):

    st.markdown('<div class="hm-heading">5 Banks × 16 Criteria</div>',unsafe_allow_html=True)

    heat = filtered.groupby(['bank','criterion']).size().unstack(fill_value=0).reindex(index=BANKS,columns=CRITERIA,fill_value=0)

    fig = px.imshow(heat,aspect='auto',text_auto=True,color_continuous_scale=['#fff6f9','#e8afc2','#a8496b','#641b38'],labels={'x':'Tiêu chí','y':'Ngân hàng','color':'Số dòng'})

    fig.update_layout(height=380,margin=dict(l=5,r=5,t=12,b=20),paper_bgcolor='rgba(0,0,0,0)',font=dict(color='#364055'))

    st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})

    st.caption('Số dòng bằng chứng không phản ánh trực tiếp mức độ chuyển đổi số hoặc điểm BDTI.')



st.markdown('<div class="hm-section">Evidence Explorer</div>',unsafe_allow_html=True)

with st.container(border=True):

    keyword = st.text_input('Tìm kiếm nội dung hoặc tên báo cáo',placeholder='Nhập từ khóa...')

    shown = filtered.copy()

    if keyword.strip():

        text = shown['context'].fillna('').astype(str)+' '+shown['filename'].fillna('').astype(str)+' '+shown['criterion_name'].fillna('').astype(str)

        shown = shown[text.str.contains(keyword.strip(),case=False,regex=False,na=False)]

    st.caption(f'Tìm thấy {len(shown):,} dòng bằng chứng')

    cols = ['bank','pillar','criterion','criterion_name','filter_stage','filename','page','context']

    st.dataframe(shown[cols],width='stretch',height=390,hide_index=True,column_config={'bank':'Ngân hàng','pillar':'Trụ cột','criterion':'Tiêu chí','criterion_name':'Tên tiêu chí','filter_stage':'Tầng lọc','filename':'Nguồn báo cáo','page':'Trang','context':st.column_config.TextColumn('Nội dung bằng chứng',width='large')})



st.caption('HerMetrics · Banking Intelligence 2025 | Evidence_Final.xlsx & ranking.csv')
