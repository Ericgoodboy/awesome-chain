
=== 结构体 Zone_ 及其依赖定义 ===

// Zone_
// 重构的xdata，资产上的可用区名称需要通过关联可用区资产来获取，加上后续会将可用区保存到资产表，这里定义和其他资产结构类似的Zone结构体
// 加下划线的原因是已经有重名的结构体了
type Zone_ struct {
	Asset
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


