
=== 结构体 Db 及其依赖定义 ===

// Db
type Db struct {
	Asset
	RegionZone
	Project
	DbInfo
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


// DbInfo
type DbInfo struct {
	BriefVpc
	BriefSubnet
	IpInfo
	PublicDomain []string `json:"publicDomain"`
	NetworkType NetworkTypeEnum `json:"networkType"`
	SecurityGroupIds
	SecurityGroup []*SecurityGroup `json:"securityGroup"`
	DbType string `json:"dbType"`
	DbSubType string `json:"dbSubType"`
	EndPointPort int `json:"endPointPort"`
	Status modelasset.StatusEnum `json:"status"`
	WhiteList []*WhiteList `json:"whiteList"`
	DbProxyEnable bool `json:"dbProxyEnable"`
	SubnetGroup []string `json:"subnetGroup"`
	SubnetGroupInfo SubnetGroupInfo `json:"subnetGroupInfo"`
	SubnetCidrList []string `json:"subnetCidrList"`
	ConfigureInfo
	ClusterType string `json:"clusterType"`
	Cluster bool `json:"cluster"`
	AutoMinorVersionUpgrade bool `json:"autoMinorVersionUpgrade"`
	BackupRetentionPeriod int32 `json:"backupRetentionPeriod"`
	CertificateExpiration int64 `json:"certificateExpiration"`
	TransportEncrypted bool `json:"transportEncrypted"`
	HighAvailability bool `json:"HighAvailability"`
	IsSafetyMode bool `json:"isSafetyMode"`
	InstanceType modelasset.DbInstanceTypeEnum `json:"instanceType"`
	NoPasswordAccess bool `json:"noPasswordAccess"`
	NotRestrictIp bool `json:"notRestrictIp"`
	Databases []*Database `json:"databases"`
	AuditSettings []*AuditSetting `json:"auditSettings"`
	FirewallRules []*FirewallRule `json:"firewallRules"`
	AutoFailover bool `json:"autoFailover"`
	KmsEncrypted bool `json:"kmsEncrypted"`
	PerformanceInsightsEnabled bool `json:"performanceInsightsEnabled"`
	DeletionProtection bool `json:"deletionProtection"`
	CopyTagsToSnapshot bool `json:"copyTagsToSnapshot"`
	IamDatabaseAuthenticationEnabled bool `json:"iamDatabaseAuthenticationEnabled"`
	StorageEncrypted bool `json:"storageEncrypted"`
	MonitoringInterval int32 `json:"monitoringInterval"`
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


// WhiteList
type WhiteList struct {
	IpList []string `json:"ipList" bson:"ipList"`
	Enable bool `json:"enable" bson:"enable"`
	Name string `json:"name" bson:"name"`
	VirtualNetworkRules []string `json:"virtualNetworkRules" bson:"virtualNetworkRules"`
}


// SubnetGroupInfo
type SubnetGroupInfo struct {
	SubnetId string `json:"subnetId" bson:"subnetId"`
	SubnetName string `json:"subnetName" bson:"subnetName"`
	RawSubnetId string `json:"rawSubnetId" bson:"rawSubnetId"`
	OriginSubnetId string `json:"originSubnetId" bson:"originSubnetId"`
}


// ConfigureInfo
type ConfigureInfo struct {
	StorageEncrypted bool `json:"storageEncrypted" bson:"storageEncrypted"`
	BackupRetentionPeriod int32 `json:"backupRetentionPeriod" bson:"backupRetentionPeriod"`
	ConfigureItems []*ConfigureItem `json:"configureItems" bson:"configureItems"`
}


// ConfigureItem
type ConfigureItem struct {
	Name string `json:"name" bson:"name"`
	Value string `json:"value" bson:"value"`
}


// Database
type Database struct {
	ID string `json:"id" bson:"id"`
	Name string `json:"name" bson:"name"`
	Tde
}


// Tde
type Tde struct {
	TdeID string `json:"tdeId" bson:"tdeId"`
	TdeName string `json:"tdeName" bson:"tdeName"`
	TransparentDataEncryptionEnabled bool `json:"transparentDataEncryptionEnabled" bson:"transparentDataEncryptionEnabled"`
}


// AuditSetting
type AuditSetting struct {
	Status string `json:"status" bson:"status"`
	RetentionDays int32 `json:"retentionDays" bson:"retentionDays"`
}


// FirewallRule
type FirewallRule struct {
	Name string `json:"name" bson:"name"`
	StartIpAddress string `json:"startIpAddress" bson:"startIpAddress"`
	EndIpAddress string `json:"endIpAddress" bson:"endIpAddress"`
}


