
=== 结构体 Mfa 及其依赖定义 ===

// Mfa
type Mfa struct {
	Asset
	MfaInfo
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


// MfaInfo
type MfaInfo struct {
	EnableDate int64 `bson:"enableDate" json:"enableDate"`
	UserId string `bson:"userId" json:"userId"`
	RootMFA bool `bson:"rootMFA" json:"rootMFA"`
}


