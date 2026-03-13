
=== 结构体 RouteTable 及其依赖定义 ===

// RouteTable
type RouteTable struct {
	Asset
	BriefRouteTable
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


// BriefRouteTable
type BriefRouteTable struct {
	Region
	BriefVpc
	BriefRouteTableIgnoreVpc
}


// Region
type Region struct {
	RegionId string `json:"regionId" bson:"regionId"`
	RegionName string `json:"regionName" bson:"regionName"`
}


// BriefVpc
type BriefVpc struct {
	VpcId string `json:"vpcId" bson:"vpcId"`
	VpcName string `json:"vpcName" bson:"vpcName"`
	RelationVpcId string `json:"relationVpcId" bson:"relationVpcId"`
	VpcCidr []string `json:"vpcCidr" bson:"vpcCidr"`
}


// BriefRouteTableIgnoreVpc
type BriefRouteTableIgnoreVpc struct {
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	AssociateType AssociateTypeEnum `json:"associateType" bson:"associateType"`
	RouterType RouterTypeEnum `json:"routerType" bson:"routerType"`
	RouteEntry []*RouteEntry `json:"routeEntry" bson:"routeEntry"`
	Default bool `json:"default" bson:"default"`
	PublicAccess bool `json:"publicAccess" bson:"publicAccess"`
	PublicNatIds []string `json:"publicNatIds" bson:"publicNatIds"`
	AssociateIgw string `json:"associateIgw" bson:"associateIgw"`
	AssociateIgwFWs []string `json:"associateIgwFWs" bson:"associateIgwFWs"`
	PublicIgwIds []string `json:"publicIgwIds" bson:"publicIgwIds"`
	PublicFWIds []string `json:"publicFWIds" bson:"publicFWIds"`
}


// RouteEntry
type RouteEntry struct {
	NextHopType NextHopTypeEnum `json:"nextHopType" bson:"nextHopType"`
	NextHopId string `json:"nextHopId" bson:"nextHopId"`
	NextHopIp string `json:"nextHopIp" bson:"nextHopIp"`
	DestinationCidr string `json:"destinationCidr" bson:"destinationCidr"`
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	RelationNextHopId string `json:"relationNextHopId" bson:"relationNextHopId"`
	SourceCidr string `json:"sourceCidr" bson:"sourceCidr"`
	IsBlackHole bool `json:"isBlackHole" bson:"isBlackHole"`
	IsCrossAccount bool `json:"isCrossAccount" bson:"isCrossAccount"`
	Name string `json:"name" bson:"name"`
}


