import os

import pandas

"""
文件格式： xlsx
表头： 规则ID	风险名称	风险类型	风险等级	云平台	合规（合并）	资产类型	规则支持时间	是否默认开启	是否有拓扑举证	风险标签	风险说明	风险影响	处置建议	风险名称（英文）	风险标签（英文）	风险说明（英文）	风险影响（英文）	处置建议（英文）  开发人  进度 文案确认状态   翻译文案状态确认
"""


class CspmModel:

    def __init__(self, **kwargs):
        self._load(**kwargs)

    def _load(self, **kwargs):
        self.id = kwargs.get('规则ID')
        self.name = kwargs.get('风险名称')
        self.type = kwargs.get('风险类型')
        self.level = kwargs.get('风险等级')
        self.platform = kwargs.get('云平台')
        self.compliance = kwargs.get('合规（合并）')
        self.asset_type = kwargs.get('资产类型')
        self.support_time = kwargs.get('规则支持时间')
        self.default_enable = kwargs.get('是否默认开启')
        self.has_topology = kwargs.get('是否有拓扑举证')
        self.tags = kwargs.get('风险标签').split(',') if kwargs.get('风险标签') and pandas.notna(
            kwargs.get('风险标签')) else []
        self.description = kwargs.get('风险说明')
        self.impact = kwargs.get('风险影响')
        self.suggestion = kwargs.get('处置建议')
        self.name_en = kwargs.get('风险名称（英文）')
        self.tags_en = kwargs.get('风险标签（英文）')
        self.description_en = kwargs.get('风险说明（英文）')
        self.impact_en = kwargs.get('风险影响（英文）')
        self.suggestion_en = kwargs.get('处置建议（英文）')
        self.dev = kwargs.get('开发人')
        self.progress = kwargs.get('进度')
        self.prompt_status = kwargs.get('文案确认状态')
        self.translate_status = kwargs.get('翻译文案状态确认')

    def to_dict(self):
        return {
            '规则id': self.id,
            '风险名称': self.name,
            '风险类型': self.type,
            '风险等级': self.level,
            '云平台': self.platform,
            '合规（合并）': self.compliance,
            '资产类型': self.asset_type,
            '规则支持时间': self.support_time,
            '是否默认开启': self.default_enable,
            '是否有拓扑举证': self.has_topology,
            '风险标签': ",".join(self.tags),
            '风险说明': self.description,
            '风险影响': self.impact,
            '处置建议': self.suggestion,
            '风险名称（英文）': self.name_en,
            '风险标签（英文）': self.tags_en,
            '风险说明（英文）': self.description_en,
            '风险影响（英文）': self.impact_en,
            '处置建议（英文）': self.suggestion_en,
            '开发人': self.dev,
            '进度': self.progress,
            '文案确认状态': self.prompt_status,
            '翻译文案状态确认': self.translate_status,
        }


class CspmFile:
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.models = []
        self._load()

    def _load(self):
        if not self.file_path:
            return
        df = pandas.read_excel(self.file_path)
        self.models = [CspmModel(**row) for _, row in df.iterrows()]

    def add_model(self, model: CspmModel):
        self.models.append(model)

    def dump(self):
        return [model.to_dict() for model in self.models]

    def dump_to_excel(self, file_path: str):
        df = pandas.DataFrame(self.dump())
        df.to_excel(file_path, index=False)


if __name__ == '__main__':
    from common import const

    cspm_file = CspmFile(os.path.join(const.BASE_DIR, 'doc', 'CSC CSPM 规则汇总_latest.xlsx'))
    cspm_file.dump_to_excel(os.path.join(const.BASE_DIR, 'doc', 'output.xlsx'))
