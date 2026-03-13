
=== 结构体 Cdn 及其依赖定义 ===

// Cdn
type Cdn struct {
	Asset
	Region
	CdnInfo
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


// CdnInfo
type CdnInfo struct {
	SslProtocol string `json:"SslProtocol" bson:"SslProtocol"`
	CdnType string `json:"cdnType" bson:"cdnType"`
	Status modelasset.StatusEnum `json:"status" bson:"status"`
}


