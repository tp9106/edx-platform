"""
Settings for Biz
"""
import json

from lms.envs.aws import CONFIG_ROOT, CONFIG_PREFIX

if 'envs' in CONFIG_ROOT:
    _CONFIG_PREFIX = CONFIG_PREFIX
else:
    _CONFIG_PREFIX = 'ga_app.'
with open(CONFIG_ROOT / _CONFIG_PREFIX + 'env.json') as env_file:
    ENV_TOKENS = json.load(env_file)

"""
Basic Settings
"""
GA_DIAGNOSIS_CHOICE01 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE01', [])
GA_DIAGNOSIS_CHOICE02 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE02', [])
GA_DIAGNOSIS_CHOICE03 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE03', [])
GA_DIAGNOSIS_CHOICE04 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE04', [])
GA_DIAGNOSIS_CHOICE05 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE05', [])
GA_DIAGNOSIS_CHOICE06 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE06', [])
GA_DIAGNOSIS_CHOICE07 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE07', [])
GA_DIAGNOSIS_CHOICE08 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE08', [])
GA_DIAGNOSIS_CHOICE09 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE09', [])
GA_DIAGNOSIS_CHOICE10 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE10', [])
GA_DIAGNOSIS_CHOICE11 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE11', [])
GA_DIAGNOSIS_CHOICE12 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE12', [])
GA_DIAGNOSIS_CHOICE13 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE13', [])
GA_DIAGNOSIS_CHOICE14 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE14', [])
GA_DIAGNOSIS_CHOICE15 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE15', [])
GA_DIAGNOSIS_CHOICE16 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE16', [])
GA_DIAGNOSIS_CHOICE17 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE17', [])
GA_DIAGNOSIS_CHOICE18 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE18', [])
GA_DIAGNOSIS_CHOICE19 = ENV_TOKENS.get('GA_DIAGNOSIS_CHOICE19', [])
GA_DIAGNOSIS_BLOCK_A1_LABEL = ENV_TOKENS.get('GA_DIAGNOSIS_BLOCK_A1_LABEL', {
    '0101': '', '0102': '', '0201': '', '0202': '', '0300': '', '0401': '', '0402': '', '0403': '', '0500': ''
})
GA_DIAGNOSIS_BLOCK_A2_AND_B1_LABEL = ENV_TOKENS.get('GA_DIAGNOSIS_BLOCK_A2_AND_B1_LABEL', {
    '01': '', '02': '', '03': '', '04': '', '05': '', '06': '', '07': '', '08': '', '09': '', '10': '',
    '11': '', '12': '', '13': '', '14': '', '15': '', '16': '', '17': '', '18': '', '19': '', '20': '',
    '21': '', '22': '', '23': '', '24': '', '25': '', '26': '', '27': ''
})
GA_DIAGNOSIS_BLOCK_A3_LABEL = ENV_TOKENS.get('GA_DIAGNOSIS_BLOCK_A3_LABEL', {
    '01': '', '02': '', '03': '', '04': '', '05': '', '06': '', '07': '', '08': '', '09': '', '10': '',
    '11': '', '12': '', '13': '', '14': '', '15': '', '16': '', '17': '', '18': '', '19': ''
})
GA_DIAGNOSIS_BLOCK_B2_LABEL = ENV_TOKENS.get('GA_DIAGNOSIS_BLOCK_B2_LABEL', {'01': '', '02': '', '03': ''})
GA_DIAGNOSIS_CHART_AB = ENV_TOKENS.get('GA_DIAGNOSIS_CHART_AB', [])
GA_DIAGNOSIS_CHART_CD = ENV_TOKENS.get('GA_DIAGNOSIS_CHART_CD', [])
GA_DIAGNOSIS_CHART_AD = ENV_TOKENS.get('GA_DIAGNOSIS_CHART_AD', [])
GA_DIAGNOSIS_CHART_BC = ENV_TOKENS.get('GA_DIAGNOSIS_CHART_BC', [])
GA_DIAGNOSIS_DATA1 = ENV_TOKENS.get('GA_DIAGNOSIS_DATA1', [])
GA_DIAGNOSIS_REGULATION = ENV_TOKENS.get('GA_DIAGNOSIS_REGULATION', {})
GA_DIAGNOSIS_DATA2 = ENV_TOKENS.get('GA_DIAGNOSIS_DATA2', [])
GA_DIAGNOSIS_SCORE_BASIS = ENV_TOKENS.get('GA_DIAGNOSIS_SCORE_BASIS', [])
GA_DIAGNOSIS_CALC_E = ENV_TOKENS.get('GA_DIAGNOSIS_CALC_E', [])
GA_DIAGNOSIS_FORM_ERROR_REASON = ENV_TOKENS.get('GA_DIAGNOSIS_FORM_ERROR_REASON', {})
GA_DIAGNOSIS_CSV_HEADER = ENV_TOKENS.get('GA_DIAGNOSIS_CSV_HEADER', None)
GA_DIAGNOSIS_CSV_FORMAT_BASE = ENV_TOKENS.get('GA_DIAGNOSIS_CSV_FORMAT_BASE', None)
GA_DIAGNOSIS_CONVERT_VALUE = ENV_TOKENS.get('GA_DIAGNOSIS_CONVERT_VALUE', None)
GA_DIAGNOSIS_MAPPING_TABLE = ENV_TOKENS.get('GA_DIAGNOSIS_MAPPING_TABLE', {})
GA_DIAGNOSIS_BLOCK3_16_REPLACE_VALUE = ENV_TOKENS.get('GA_DIAGNOSIS_BLOCK3_16_REPLACE_VALUE', None)
GA_DIAGNOSIS_OUTPUT_FILE_FORMAT = ENV_TOKENS.get('GA_DIAGNOSIS_OUTPUT_FILE_FORMAT', None)
GA_DIAGNOSIS_OUTPUT_BUCKET_NAME = ENV_TOKENS.get('GA_DIAGNOSIS_OUTPUT_BUCKET_NAME', None)
GA_DIAGNOSIS_ACCESS_KEY_ID = ENV_TOKENS.get('GA_DIAGNOSIS_ACCESS_KEY_ID', None)
GA_DIAGNOSIS_SECRET_ACCESS_KEY = ENV_TOKENS.get('GA_DIAGNOSIS_SECRET_ACCESS_KEY', None)
GA_DIAGNOSIS_EXCLUDE_TARGET_DATA = ENV_TOKENS.get('GA_DIAGNOSIS_EXCLUDE_TARGET_DATA', None)
GA_DIAGNOSIS_AUTO_ENROLLMENT_COURSES = ENV_TOKENS.get('GA_DIAGNOSIS_AUTO_ENROLLMENT_COURSES', [])
GA_DIAGNOSIS_STANDARD_AVERAGE_CODE = ENV_TOKENS.get('GA_DIAGNOSIS_STANDARD_AVERAGE_CODE', None)
GA_DIAGNOSIS_CONTRACT_ID = ENV_TOKENS.get('GA_DIAGNOSIS_CONTRACT_ID', None)
GA_DIAGNOSIS_SERVICE_SUPPORT_SENDER = ENV_TOKENS.get('GA_DIAGNOSIS_SERVICE_SUPPORT_SENDER', None)
GA_DIAGNOSIS_SERVICE_SUPPORT_EMAIL = ENV_TOKENS.get('GA_DIAGNOSIS_SERVICE_SUPPORT_EMAIL', [])
GA_DIAGNOSIS_ALLOW_COURSE_ID_LIST = ENV_TOKENS.get('GA_DIAGNOSIS_ALLOW_COURSE_ID_LIST', [])
