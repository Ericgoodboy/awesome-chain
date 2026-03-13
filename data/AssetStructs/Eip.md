
=== 结构体 Eip 及其依赖定义 ===

// Eip
type Eip struct {
	Asset
	EipInfo
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


// EipInfo
type EipInfo struct {
	Region
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	Ip string `json:"ip" bson:"ip"`
	InstanceId string `json:"instanceId" bson:"instanceId"`
	RelationInstanceId string `json:"relationInstanceId" bson:"relationInstanceId"`
	Type string `json:"type" bson:"type"`
}


// Region
type Region struct {
	RegionId string `json:"regionId" bson:"regionId"`
	RegionName string `json:"regionName" bson:"regionName"`
}


