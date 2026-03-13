
=== 结构体 LoadBalance 及其依赖定义 ===

// LoadBalance
type LoadBalance struct {
	Asset
	BriefVpc
	Region
	Project
	IpInfo
	AssetTag []string `json:"assetTag" bson:"assetTag"`
	Domain string
	MasterZoneId string `json:"masterZoneId"`
	SlaveZoneId string `json:"slaveZoneId"`
	Status modelasset.StatusEnum `json:"status"`
	AddressType AddressTypeEnum `json:"addressType"`
	Type string `json:"Type"`
	ListenerList []*LoadBalanceListener `json:"listenerList"`
	SecurityGroupIds []*string `json:"securityGroupIds"`
	Http2Enabled bool `json:"http2Enabled"`
	SubnetGroup []string `json:"subnetGroup"`
	PublicFWIds []string `json:"publicFWIds" bson:"publicFWIds"`
	InNatRules []*InNatRule `json:"inNatRules"`
	OutNatRules []*OutNatRule `json:"outNatRules"`
	CrossZoneLoadBalancing bool `json:"crossZoneLoadBalancing"`
	AccessLogsEnabled bool `json:"accessLogsEnabled"`
	DeletionProtection bool `json:"deletionProtection"`
	DesyncMitigationMode string `json:"desyncMitigationMode"`
	DropInvalidHeaderFields bool `json:"dropInvalidHeaderFields"`
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


// IpInfo
type IpInfo struct {
	PublicIp []string `json:"publicIp" bson:"publicIp"`
	PrivateIp []string `json:"privateIp" bson:"privateIp"`
}


// LoadBalanceListener
type LoadBalanceListener struct {
	ListenerId string
	ListenerName string
	Status modelasset.StatusEnum
	ListenerProtocol modelasset.LoadBalanceProtocolEnum
	ListenerPort int32
	FrontServer []*LoadBalanceListenerBackendServer
	BackendServer []*LoadBalanceListenerBackendServer
	AclType modelasset.AclTypeEnum
	AclList []*LoadBalanceAclInfo
	SslPolicy string
	Priority int32
	Action []*Action `json:"action"`
	ForwardTargetEnable bool
}


// LoadBalanceListenerBackendServer
type LoadBalanceListenerBackendServer struct {
	InstanceId string
	InstanceName string
	EthId string
	Ports []int32
	Status modelasset.StatusEnum
	Address string
	GroupId string
	GroupName string
	InstanceVpcId string
}


// LoadBalanceAclInfo
type LoadBalanceAclInfo struct {
	Status modelasset.StatusEnum `json:"status" `
	Id string `json:"id" `
	Name string `json:"name" `
	AllIp bool `json:"allIp" `
	IpArray []*AclIpAddrInfo `json:"ipArray" `
}


// AclIpAddrInfo
type AclIpAddrInfo struct {
	Status modelasset.StatusEnum `json:"status"`
	Ip string `json:"ip"`
}


// Action
type Action struct {
	Protocol modelasset.LoadBalanceProtocolEnum `json:"protocol"`
	ActionType ActionTypeEnum `json:"actionType"`
}


// InNatRule
// InNatRule LB的DNat 规则
type InNatRule struct {
	Id string `json:"id"`
	Name string `json:"name"`
	Status modelasset.StatusEnum `json:"status"`
	FrontIp string `json:"frontIp"`
	FrontPort *modelasset.PortRange `json:"frontPort"`
	BackendServer []*LoadBalanceListenerBackendServer `json:"backendServer"`
	BackendPort int32 `json:"backendPort"`
	Protocol string `json:"protocol"`
}


// OutNatRule
// OutNatRule LB的SNat 规则
type OutNatRule struct {
	Id string `json:"id"`
	Name string `json:"name"`
	Status modelasset.StatusEnum `json:"status"`
	SNatIp []string `json:"sNatIp"`
	SrcServer []*LoadBalanceListenerBackendServer `json:"SrcServer"`
	Protocol string `json:"protocol"`
}


