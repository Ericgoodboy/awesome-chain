
=== 结构体 IPsec 及其依赖定义 ===

// IPsec
type IPsec struct {
	Asset
	Region
	IPsecInfo
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


// IPsecInfo
type IPsecInfo struct {
	IPsecId string `json:"ipsecId" bson:"ipsecId"`
	IPsecName string `json:"ipsecName" bson:"ipsecName"`
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	LocalPublicIp string `json:"localPublicIp" bson:"localPublicIp"`
	RemotePublicIp string `json:"remotePublicIp" bson:"remotePublicIp"`
	LocalId string `json:"localId" bson:"localId"`
	RemoteId string `json:"remoteId" bson:"remoteId"`
	Psk string `json:"psk" bson:"psk"`
	AttachType IPsecAttachTypeEnum `json:"attachType" bson:"attachType"`
	AttachInstanceId string `json:"attachInstanceId" bson:"attachInstanceId"`
	AttachInstanceCenId string `json:"attachInstanceCenId" bson:"attachInstanceCenId"`
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


