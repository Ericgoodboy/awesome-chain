
=== 结构体 AcPolicy 及其依赖定义 ===

// AcPolicy
// 访问控制策略
type AcPolicy struct {
	Asset
	AcPolicyInfo
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


// AcPolicyInfo
type AcPolicyInfo struct {
	Type PolicyType `json:"type" bson:"type"`
	Version string `json:"version" bson:"version"`
	Document *AcPolicyDocument `json:"document" bson:"document"`
}


// AcPolicyDocument
type AcPolicyDocument struct {
	Version string `json:"version" bson:"version"`
	Statements []*AcPolicyStatement `json:"statements" bson:"statements"`
}


// AcPolicyStatement
type AcPolicyStatement struct {
	Principal string `json:"principal" bson:"principal"`
	Effect EffectEnum `json:"effect" bson:"effect"`
	Action []string `json:"action" bson:"action"`
	NotAction []string `json:"notAction" bson:"notAction"`
	Resource []string `json:"resource" bson:"resource"`
	Condition string `json:"condition" bson:"condition"`
	NotResource []string `json:"notResource" bson:"notResource"`
	NotPrincipal string `json:"notPrincipal" bson:"notPrincipal"`
}


