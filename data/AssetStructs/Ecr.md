
=== 结构体 Ecr 及其依赖定义 ===

// Ecr
type Ecr struct {
	Asset
	Region
	Project
	BriefVpc
	EcrInfo
	AssetTag []string `json:"assetTag" bson:"assetTag"`
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


// BriefVpc
type BriefVpc struct {
	VpcId string `json:"vpcId" bson:"vpcId"`
	VpcName string `json:"vpcName" bson:"vpcName"`
	RelationVpcId string `json:"relationVpcId" bson:"relationVpcId"`
	VpcCidr []string `json:"vpcCidr" bson:"vpcCidr"`
}


// EcrInfo
type EcrInfo struct {
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	AssociationList []*Association `json:"associationList" bson:"associationList"`
	IsCenAssociated bool `json:"isCenAssociated" bson:"isCenAssociated"`
	IsAliEcr bool `json:"isAliEcr" bson:"isAliEcr"`
	IpInfo IpInfo `json:"ipInfo" bson:"ipInfo"`
	RouteTableId string `json:"routeTableId" bson:"routeTableId"`
	RouteEntry []*EcrRouteEntry `json:"routeEntry" bson:"routeEntry"`
	DirectConnectInterface []*DirectConnectInterface `json:"directConnectInterface" bson:"directConnectInterface"`
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


// IpInfo
type IpInfo struct {
	PublicIp []string `json:"publicIp" bson:"publicIp"`
	PrivateIp []string `json:"privateIp" bson:"privateIp"`
}


// EcrRouteEntry
type EcrRouteEntry struct {
	RouteEntry
	DirectConnectInfo
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


// DirectConnectInfo
type DirectConnectInfo struct {
	PrivateLocalIp string `json:"privateLocalIp"`
	PrivateRemoteIp string `json:"privateRemoteIp"`
}


// DirectConnectInterface
type DirectConnectInterface struct {
	// 专线接口ID
	Id string `json:"id" bson:"id"`
	// 本端互联IP（一般指云上专线网关互联IP）
	PrivateLocalIp string `json:"privateLocalIp" bson:"privateLocalIp"`
	// 对端互联IP（一般指客户本地侧IDC网关互联IP）
	PrivateRemoteIp string `json:"privateRemoteIp" bson:"privateRemoteIp"`
	// 当前专线接口所对应的用户侧的网段列表，当前仅腾讯云有值
	// 这个列表里的网段理论上需要和专线网关路由条目里的网段相匹配
	RemoteRoutePrefixes []string `json:"remoteRoutePrefixes" bson:"remoteRoutePrefixes"`
}


