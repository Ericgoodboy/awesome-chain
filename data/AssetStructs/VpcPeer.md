
=== 结构体 VpcPeer 及其依赖定义 ===

// VpcPeer
type VpcPeer struct {
	Asset
	VpcPeerInfo
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


// VpcPeerInfo
type VpcPeerInfo struct {
	Region
	Description string `json:"description" bson:"description"`
	Vpc VpcPeerVpcInfo `json:"vpc" bson:"vpc"`
	AcceptingVpc VpcPeerVpcInfo `json:"acceptingVpc" bson:"acceptingVpc"`
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	IsCrossAccount bool `json:"isCrossAccount" bson:"isCrossAccount"`
}


// Region
type Region struct {
	RegionId string `json:"regionId" bson:"regionId"`
	RegionName string `json:"regionName" bson:"regionName"`
}


// VpcPeerVpcInfo
type VpcPeerVpcInfo struct {
	BriefVpc
	CloudAccountId string `json:"cloudAccountId" bson:"cloudAccountId"`
}


// BriefVpc
type BriefVpc struct {
	VpcId string `json:"vpcId" bson:"vpcId"`
	VpcName string `json:"vpcName" bson:"vpcName"`
	RelationVpcId string `json:"relationVpcId" bson:"relationVpcId"`
	VpcCidr []string `json:"vpcCidr" bson:"vpcCidr"`
}


