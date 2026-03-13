
=== 结构体 Ecs 及其依赖定义 ===

// Ecs
type Ecs struct {
	Asset
	BriefVpc
	BriefSubnet
	RegionZone
	Project
	IpInfo
	SecurityGroupIds
	AssetTag []string `json:"assetTag" bson:"assetTag"`
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	CloudSource int64 `json:"cloudSource" bson:"cloudSource"`
	OsType OsTypeEnum `json:"osType" bson:"osType"`
	OsTypeDetail string `json:"osTypeDetail" bson:"osTypeDetail"`
	NetWorkInterface []*NetWorkInterface `json:"netWorkInterface" bson:"netWorkInterface"`
	EipTransfer bool `json:"eipTransfer" bson:"eipTransfer"`
	PublicAccess bool `json:"publicAccess" bson:"publicAccess"`
	PublicImages bool `json:"publicImages" bson:"publicImages"`
	PublicNatIds []string `json:"publicNatIds" bson:"publicNatIds"`
	PublicFWIds []string `json:"publicFWIds" bson:"publicFWIds"`
	IMDSv2Status bool `json:"IMDSv2Status" bson:"IMDSv2Status"`
	UserData string `json:"UserData" bson:"UserData"`
	KeyPairName string `json:"keyPairName" bson:"keyPairName"`
	SecurityProfile *SecurityProfile `json:"securityProfile" bson:"securityProfile"`
	HasInstanceProfile bool `json:"hasInstanceProfile" bson:"hasInstanceProfile"`
	RoleName string `json:"roleName" bson:"roleName"`
	RoleId string `json:"roleId" bson:"roleId"`
	BindRoleArn string `json:"bindRoleArn" bson:"bindRoleArn"`
	MetadataOption MetadataOption `json:"metadataOption" bson:"metadataOption"`
	EbsOptimized bool `json:"ebsOptimized" bson:"ebsOptimized"`
	MonitorEnable bool `json:"monitorEnable" bson:"monitorEnable"`
	BriefSasProtection BriefSasProtection `json:"briefSasProtection"`
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


// RegionZone
type RegionZone struct {
	Region
	Zone
}


// Region
type Region struct {
	RegionId string `json:"regionId" bson:"regionId"`
	RegionName string `json:"regionName" bson:"regionName"`
}


// Zone
type Zone struct {
	ZoneId string `json:"zoneId" bson:"zoneId"`
	ZoneName string `json:"zoneName" bson:"zoneName"`
}


// Project
type Project struct {
	ProjectId string `json:"projectId" bson:"projectId"`
	ProjectName string `json:"projectName" bson:"projectName"`
	ProjectParentId string `json:"projectParentId" bson:"projectParentId"`
}


// IpInfo
type IpInfo struct {
	PublicIp []string `json:"publicIp" bson:"publicIp"`
	PrivateIp []string `json:"privateIp" bson:"privateIp"`
}


// NetWorkInterface
type NetWorkInterface struct {
	NetWorkInterfaceId string `json:"netWorkInterfaceId" bson:"netWorkInterfaceId"`
	AppSecGroupIds []string `json:"appSecGroupIds" bson:"appSecGroupIds"`
	Primary bool `json:"primary" bson:"primary"`
}


// SecurityProfile
type SecurityProfile struct {
	SecurityType string `json:"securityType"`
	UefiSettings
}


// UefiSettings
type UefiSettings struct {
	SecureBootEnabled bool `json:"secureBootEnabled"`
	VTpmEnabled bool `json:"vTpmEnabled"`
}


// MetadataOption
type MetadataOption struct {
	// 关闭元数据服务端点
	DisableEndpoint bool
	// 访问元数据必须携带token(强制IMDSv2)
	TokenRequired bool
}


// BriefSasProtection
type BriefSasProtection struct {
	RelationSasId string `json:"relationSasId" bson:"relationSasId"`
	AgentStatus AgentStatusEnum `json:"agentStatus" bson:"agentStatus"`
	ProtectVersion string `json:"protectVersion" bson:"protectVersion"`
}


