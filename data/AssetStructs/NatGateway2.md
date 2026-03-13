
=== 结构体 NatGateway2 及其依赖定义 ===

// NatGateway2
// NatGateway2 上报xdr格式
type NatGateway2 struct {
	Asset
	Region
	Project
	BriefVpc
	BriefSubnet
	IpInfo
	SecurityGroupIds
	SecurityGroup []*SecurityGroup `json:"securityGroup"`
	NetworkType AddressTypeEnum `json:"networkType"`
	DNatTableIds []string `json:"DNatTableIds"`
	// DNatRoute        []*DNatRoute              `json:"DNatRoute"`     // NDat转发条目
	Status modelasset.StatusEnum `json:"status"`
	NatGatewayData NatGatewayData `bson:"data" json:"data"`
	CreateTimeStamp int64 `bson:"createTime"`
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


// SecurityGroup
type SecurityGroup struct {
	Asset
	Region
	Rule SecRules `json:"rule" bson:"rule"`
	InnerAccessPolicy string `json:"innerAccessPolicy" bson:"innerAccessPolicy"`
	Priority int32 `json:"priority" bson:"priority"`
}


// NatGatewayData
type NatGatewayData struct {
	DNatRoute []DNatTable `bson:"DNatRoute" json:"DNatRoute"`
	SNatRoute []SNatTable `bson:"SNatRoute" json:"SNatRoute"`
}


// DNatTable
type DNatTable struct {
	ForwardEntryId string `json:"forwardEntryId"`
	IpProtocol string `json:"ipProtocol"`
	ExternalIp string `json:"externalIp"`
	ExternalPort modelasset.PortRange `json:"externalPort"`
	InternalIp string `json:"internalIp"`
	InternalPort modelasset.PortRange `json:"internalPort"`
	Status string `json:"status"`
}


// SNatTable
type SNatTable struct {
	SnatEntryId string `bson:"SnatEntryId" json:"SnatEntryId"`
	SourceCIDR string `bson:"sourceCIDR" json:"sourceCIDR"`
	SnatIp string `bson:"snatIp" json:"snatIp"`
	Status string `bson:"status" json:"status"`
}


