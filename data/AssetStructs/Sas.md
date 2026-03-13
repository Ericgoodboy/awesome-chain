
=== 结构体 Sas 及其依赖定义 ===

// Sas
type Sas struct {
	Asset
	EcsProtectNum int32 `json:"ecsProtectNum" bson:"ecsProtectNum"`
	LocalRegion string `json:"-"`
	SasAssetList []*SasProtection `json:"sasAssetList" bson:"sasAssetList"`
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


// SasProtection
type SasProtection struct {
	InstanceId string `json:"instanceId" bson:"instanceId"`
	BriefSasProtection
}


// BriefSasProtection
type BriefSasProtection struct {
	RelationSasId string `json:"relationSasId" bson:"relationSasId"`
	AgentStatus AgentStatusEnum `json:"agentStatus" bson:"agentStatus"`
	ProtectVersion string `json:"protectVersion" bson:"protectVersion"`
}


