import io
import pandas as pd

df = pd.read_fwf(
    'gs_case.txt',
    encoding='latin-1',
    widths=[
        10, 10, 10, 1, 50, 11, 1, 1, 4, 2, 2, 1, 2, 3, 15, 4, 11, 4, 4, 2, 1, 2, 1, 11, 11, 25, 20, 20, 1, 11, 11, 1, 11, 11, 1, 1, 1, 11, 1, 1, 11, 30, 11, 30
])
print(df.head(2))

# GS_CASE - 383 Characters    
# | FieldName            | FieldType    | Position (From:To) |
# | -------------------- | ------------ | ------------------ |
# | **DISTRICT**         | VARCHAR2(10) | (001:010)          |
# | **CASEID**           | VARCHAR2(10) | (011:020)          |
# | **TR1_UNIQUEID**     | VARCHAR2(10) | (021:030)          |
# | **CLASS**            | VARCHAR2(1)  | (031:031)          |
# | **NAME**             | VARCHAR2(50) | (032:081)          |
# | **RECVD_DATE**       | DATE(11)     | (082:092)          |
# | **SECURITY**         | VARCHAR2(1)  | (093:093)          |
# | **PRIORITY**         | VARCHAR2(1)  | (094:094)          |
# | **TYPE**             | VARCHAR2(4)  | (095:098)          |
# | **US_ROLE**          | VARCHAR2(2)  | (099:100)          |
# | **LIT_RESP**         | VARCHAR2(2)  | (101:102)          |
# | **LIT_TRACK**        | VARCHAR2(1)  | (103:103)          |
# | **WEIGHT**           | VARCHAR2(2)  | (104:105)          |
# | **BRANCH**           | VARCHAR2(3)  | (106:108)          |
# | **GRAND_JURY_NUM**   | VARCHAR2(15) | (109:123)          |
# | **UNIT**             | VARCHAR2(4)  | (124:127)          |
# | **DCMNS_NUMBER**     | VARCHAR2(11) | (128:138)          |
# | **TRIBE**            | VARCHAR2(4)  | (139:142)          |
# | **RESERVATION**      | VARCHAR2(4)  | (143:146)          |
# | **SPEC_PROJ**        | VARCHAR2(2)  | (147:148)          |
# | **VIC_WIT**          | VARCHAR2(1)  | (149:149)          |
# | **ADR_MODE**         | VARCHAR2(2)  | (150:151)          |
# | **COLLECT_IND**      | VARCHAR2(1)  | (152:152)          |
# | **OFFENSE_FROM**     | DATE(11)     | (153:163)          |
# | **OFFENSE_TO**       | DATE(11)     | (164:174)          |
# | **LEAD_CHARGE**      | VARCHAR2(25) | (175:199)          |
# | **PHYSICAL_LOC**     | VARCHAR2(20) | (200:219)          |
# | **STORE_NUM**        | VARCHAR2(20) | (220:239)          |
# | **CIVIL_POTEN**      | VARCHAR2(1)  | (240:240)          |
# | **SYS_INIT_DATE**    | DATE(11)     | (241:251)          |
# | **ACCESS_DATE**      | DATE(11)     | (252:262)          |
# | **STATUS**           | VARCHAR2(1)  | (263:263)          |
# | **CLOSE_DATE**       | DATE(11)     | (264:274)          |
# | **DEST_DATE**        | DATE(11)     | (275:285)          |
# | **PERMANENT**        | VARCHAR2(1)  | (286:286)          |
# | **CASE_RESTRICTED**  | VARCHAR2(1)  | (287:287)          |
# | **CRIMINAL_POTEN**   | VARCHAR2(1)  | (288:288)          |
# | **TOT_VICTIMS**      | VARCHAR2(11) | (289:299)          |
# | **RELATED_FLU_FLAG** | VARCHAR2(1)  | (300:300)          |
# | **QUI_TAM**          | VARCHAR2(1)  | (301:301)          |
# | **CREATE_DATE**      | DATE(11)     | (302:312)          |
# | **CREATE_USER**      | VARCHAR2(30) | (313:342)          |
# | **UPDATE_DATE**      | DATE(11)     | (343:353)          |
# | **UPDATE_USER**      | VARCHAR2(30) | (354:383)          |

# AK        1983V01272          VState of Alaska (v. U.S.)                         06-JUL-1983*     D DJ   1  *                  97-627063-0             N                                               *                   *                   *31-AUG-199115-FEB-2000C15-FEB-200012-FEB-2010N**             17-NOV-2006*                                                     