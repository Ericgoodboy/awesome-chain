
=== 结构体 Cen 及其依赖定义 ===

// Cen
type Cen struct {
	Asset
	Region
	CenInfo
	AssetTag []string `json:"assetTag" bson:"assetTag"`
	Project
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


// CenInfo
type CenInfo struct {
	RealName CenRealNameEnum `json:"realName" bson:"realName"`
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	TransitRouterList []*TransitRouter `json:"transitRouterList" bson:"transitRouterList"`
}


// TransitRouter
type TransitRouter struct {
	TransitRouterId string `json:"transitRouterId" bson:"transitRouterId"`
	TransitRouterName string `json:"transitRouterName" bson:"transitRouterName"`
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	AssociationList []*Association `json:"associationList" bson:"associationList"`
	Region
	RouteTableList []*TransitRouterRouteTable `json:"routeTableList" bson:"routeTableList"`
}


// Association
type Association struct {
	InstanceId string `json:"instanceId" bson:"instanceId"`
	InstanceType AssociationTypeEnum `json:"instanceType" bson:"instanceType"`
	DefaultAccess bool `json:"defaultAccess" bson:"defaultAccess"`
	CloudAccountId string `json:"cloudAccountId" bson:"cloudAccountId"`
	IsCrossAccount bool `json:"isCrossAccount" bson:"isCrossAccount"`
	// 以下字段仅当资产类型为云企业网时才生效
	CenRouteTableId string `json:"cenRouteTableId" bson:"cenRouteTableId"`
	// 以下字段仅当资产类型为云企业网时才生效，目前仅在阿里云使用
	// 功能简介：在阿里云上，转发路由器和 VPC 关联本质上是建立了一个连接，VPC 路由表中路由条目的下一跳的实例是这个连接ID
	// 拓扑计算业务需要 VPC 路由表中路由条目的下一跳是转发路由器的 ID，而非连接 ID
	// 因此需要记录这个连接ID，在关联层实现对 VPC 路由条目的 ID 修改
	TransitRouterAttachmentId string `json:"transitRouterAttachmentId" bson:"transitRouterAttachmentId"`
}


// TransitRouterRouteTable
type TransitRouterRouteTable struct {
	RouteTableId string `json:"routeTableId" bson:"routeTableId"`
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	Default bool `json:"default" bson:"default"`
	RouteEntry []*RouteEntry `json:"routeEntry" bson:"routeEntry"`
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


// Project
type Project struct {
	ProjectId string `json:"projectId" bson:"projectId"`
	ProjectName string `json:"projectName" bson:"projectName"`
	ProjectParentId string `json:"projectParentId" bson:"projectParentId"`
}


