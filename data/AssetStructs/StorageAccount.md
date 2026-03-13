
=== 结构体 StorageAccount 及其依赖定义 ===

// StorageAccount
type StorageAccount struct {
	Asset
	Region
	Project
	AssetTag []string `json:"assetTag" bson:"assetTag"`
	Domain string `json:"domain"`
	PublicAccessBlock bool `json:"publicAccessBlock"`
	BucketType string `json:"bucketType"`
	MinimumTlsVersion string `json:"minimumTLSVersion"`
	TransportEncrypted bool `json:"transportEncrypted"`
	KeyExpirationPeriod int32 `json:"keyExpirationPeriod"`
	EncryptionType string `json:"encryptionType"`
	InfrastructureEncryption bool `json:"infrastructureEncryption"`
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


// Project
type Project struct {
	ProjectId string `json:"projectId" bson:"projectId"`
	ProjectName string `json:"projectName" bson:"projectName"`
	ProjectParentId string `json:"projectParentId" bson:"projectParentId"`
}


