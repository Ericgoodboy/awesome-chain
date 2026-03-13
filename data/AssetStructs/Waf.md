
=== 结构体 Waf 及其依赖定义 ===

// Waf
type Waf struct {
	Asset
	Region
	WafInfo
}


// Asset
// Asset 资产
type Asset struct {
	TenantId int64 `json:"tenantId"`
	CloudAccountId string `json:"cloudAccountId"`
	ResourceType string `json:"resourceType"`
	Source string `json:"source"`
	LocalRegion string `json:"-"`
	RawAssetInfo
}


// RawAssetInfo
type RawAssetInfo struct {
	RawId string `json:"rawId"`
	RawIdShow string `json:"rawIdShow"`
	Name string `json:"name"`
	CreateTime time.Time `json:"createTime"`
	AssetVersion string `json:"assetVersion"`
}


// Region
type Region struct {
	RegionId string `json:"regionId" bson:"regionId"`
	RegionName string `json:"regionName" bson:"regionName"`
}


// WafInfo
type WafInfo struct {
	Status modelasset.StatusEnum
	ProtectObjects []*WafProtectObject
	RuleTemplates []*WafRuleTemplate
	ForwardOriginIpList []string
	LogEnabled bool `json:"logEnabled" bson:"logEnabled"`
}


// WafProtectObject
type WafProtectObject struct {
	InstanceId string
	InstanceIp string
	ObjectName string
	ProductType WafProductTypeEnum
	AccessMethod WafAccessMethodTypeEnum
	ProtectStatus modelasset.StatusEnum
	Http2Enabled bool
	ProtectProtocolPorts []*WafProtocolPort
	Domain string
	OriginServers []*WafOriginServer
	RelationRuleTemplates []*WafRelationRuleTemplate
	AllTraffic bool
	CompleteProtect bool
	InstanceSubIds []string
}


// WafProtocolPort
type WafProtocolPort struct {
	Protocol modelasset.ProtocolEnum
	Ports []int32
}


// WafOriginServer
type WafOriginServer struct {
	Address string
	AddressType WafOriginServerAddressTypeEnum
	ForwardOrigins []*WafForwardOrigin
}


// WafForwardOrigin
type WafForwardOrigin struct {
	ForwardOriginAddress []string
	ForwardOriginProtocolPorts []*WafProtocolPort
}


// WafRelationRuleTemplate
type WafRelationRuleTemplate struct {
	RuleModuleType WafRuleModuleTypeEnum
	TemplateIds []string
}


// WafRuleTemplate
type WafRuleTemplate struct {
	RuleModuleType WafRuleModuleTypeEnum
	TemplateName string
	TemplateId string
	IsDefault bool
	Status modelasset.StatusEnum
	Action modelasset.ActionEnum
	Rules []*WafRule
	SubRuleTemplates []*WafSubRuleTemplate
	Priority int32
}


// WafRule
// 防护规则统一结构
type WafRule struct {
	RuleId string
	Status modelasset.StatusEnum
	Action modelasset.ActionEnum
	RuleConditions []*WafRuleCondition
	NoAllDetection bool
}


// WafRuleCondition
// 匹配条件
type WafRuleCondition struct {
	Key WafRuleConditionKeyEnum
	SubKey string
	OpValue WafRuleConditionOpValueEnum
	Value []string
}


// WafSubRuleTemplate
type WafSubRuleTemplate struct {
	RuleModuleType WafRuleModuleTypeEnum
	Status modelasset.StatusEnum
	Action modelasset.ActionEnum
	Rules []*WafRule
}


