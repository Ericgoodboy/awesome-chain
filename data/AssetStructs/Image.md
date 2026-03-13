
=== 结构体 Image 及其依赖定义 ===

// Image
type Image struct {
	Asset
	Region
	SnapshotInfo
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


// SnapshotInfo
type SnapshotInfo struct {
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	Encrypted bool `json:"encrypted" bson:"encrypted"`
	SnapshotType SnapshotType `json:"snapshotType" bson:"snapshotType"`
	Public bool `json:"public" bson:"public"`
}


