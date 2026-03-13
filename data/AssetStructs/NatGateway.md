
=== 结构体 NatGateway 及其依赖定义 ===

// NatGateway
type NatGateway struct {
	Asset
	Region
	Project
	BriefVpc
	BriefSubnet
	IpInfo
	SecurityGroupIds
	AssetTag []string `json:"assetTag" bson:"assetTag"`
	NetworkType AddressTypeEnum `json:"networkType" bson:"networkType"`
	DNatTableIds []string `json:"DNatTableIds" bson:"DNatTableIds"`
	DNatRoute []*DNatRoute `json:"DNatRoute" bson:"DNatRoute"`
	SNatTableIds []string `json:"SNatTableIds" bson:"SNatTableIds"`
	SNatRoute []*SNatRoute `json:"SNatRoute" bson:"SNatRoute"`
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	PublicAccess bool `json:"publicAccess" bson:"publicAccess"`
	PublicFWIds []string `json:"publicFWIds" bson:"publicFWIds"`
	EffectedSubnetIds []string `json:"effectedSubnetIds" bson:"effectedSubnetIds"`
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


// BriefSubnet
type BriefSubnet struct {
	SubnetId string `json:"subnetId" bson:"subnetId"`
	SubnetName string `json:"subnetName" bson:"subnetName"`
	RelationSubnetId string `json:"relationSubnetId" bson:"relationSubnetId"`
	PublicAccess bool `json:"publicAccess" bson:"publicAccess"`
	SubnetCidr string `json:"subnetCidr" bson:"subnetCidr"`
}


// IpInfo
type IpInfo struct {
	PublicIp []string `json:"publicIp" bson:"publicIp"`
	PrivateIp []string `json:"privateIp" bson:"privateIp"`
}


// DNatRoute
type DNatRoute struct {
	InternalIp string `json:"internalIp" bson:"internalIp"`
	InternalPort *modelasset.PortRange
	ExternalIp string `json:"externalIp" bson:"externalIp"`
	ExternalPort *modelasset.PortRange
	Status string `json:"status" bson:"status"`
	ForwardEntryId string `json:"forwardEntryId" bson:"forwardEntryId"`
	ForwardEntryName string `json:"forwardEntryName" bson:"forwardEntryName"`
	IpProtocol string `json:"ipProtocol" bson:"ipProtocol"`
}


// SNatRoute
type SNatRoute struct {
	SourceSubnetId string `json:"sourceSubnetId" bson:"sourceSubnetId"`
	RelationSubnetId string `json:"relationSubnetId" bson:"relationSubnetId"`
	Status string `json:"status" bson:"status"`
	SnatEntryId string `json:"SnatEntryId" bson:"SnatEntryId"`
	SnatEntryName string `json:"SnatEntryName" bson:"SnatEntryName"`
	SourceCIDR string `json:"sourceCIDR" bson:"sourceCIDR"`
	ResourceId string `json:"resourceId" bson:"resourceId"`
	ResourceType NatGatewayResourceTypeEnum `json:"resourceType" bson:"resourceType"`
	RelationResourceId string `json:"relationResourceId" bson:"relationResourceId"`
	SnatIp string `json:"snatIp" bson:"snatIp"`
}


