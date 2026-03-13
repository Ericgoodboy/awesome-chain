
=== 结构体 OssBucket 及其依赖定义 ===

// OssBucket
type OssBucket struct {
	Asset
	Region
	Project
	AssetTag []string `json:"assetTag" bson:"assetTag"`
	Domain string `json:"domain"`
	DataRedundancyType string `json:"dataRedundancyType"`
	SSEAlgorithm string `json:"SSEAlgorithm"`
	Grant []*Grant `json:"grant"`
	Policy OSSPolicy `json:"policy"`
	Referer Referer `json:"referer"`
	GlobalPublicAccessBlock bool `json:"globalPublicAccessBlock"`
	PublicAccessBlock bool `json:"publicAccessBlock"`
	NotificationConfig bool `json:"notificationConfig"`
	MfaDelete bool `json:"mfaDelete"`
	BucketType string `json:"bucketType"`
	StorageClass string `json:"storageClass"`
	PolicyStatus bool `json:"policyStatus"`
	MinimumTlsVersion string `json:"minimumTLSVersion"`
	TransportEncrypted bool `json:"transportEncrypted"`
	KeyExpirationPeriod int32 `json:"keyExpirationPeriod"`
	AccessBlock
	ActionSupportWideCard bool `json:"actionSupportWideCard"`
	ConditionSupportWideCard bool `json:"conditionSupportWideCard"`
	ReplicationEnable bool `json:"replicationEnable"`
	VersioningEnable bool `json:"versioningEnable"`
	LifecycleEnable bool `json:"lifecycleEnable"`
	LoggingEnable bool `json:"loggingEnable"`
	// OSS 拉取是否遇到权限错误,为后序CSPM计算逻辑提供字段,因权限拉取失败则不进行计算
	HasInternalPermissionError bool `json:"hasInternalPermissionError" bson:"hasInternalPermissionError"`
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


// Grant
type Grant struct {
	Grant string `json:"grant"`
	Grantee string `json:"grantee"`
}


// OSSPolicy
type OSSPolicy struct {
	Statement []*OSSStatement `json:"statement"`
	Version string `json:"version,omitempty"`
}


// OSSStatement
type OSSStatement struct {
	Effect string `json:"effect" bson:"effect"`
	Action []string `json:"action" bson:"action"`
	NotAction []string `json:"notAction" bson:"notAction"`
	Principal string `json:"principal" bson:"principal"`
	NotPrincipal string `json:"notPrincipal" bson:"notPrincipal"`
	Resource []string `json:"resource" bson:"resource"`
	NotResource []string `json:"notResource" bson:"notResource"`
	Condition *Condition `json:"condition" bson:"condition"`
	Sid string `json:"sid" bson:"sid"`
	PrivateData interface{} `json:"privatedata" bson:"privatedata"`
}


// Condition
type Condition struct {
	IpAddress []string
	InternetIpAddress []string
	NotIpAddress []string
	NotInternetIpAddress []string
	SourceVpc []string
	NotSourceVpc []string
	SourceVpcIgnoreCase []string
	NotSourceVpcIgnoreCase []string
	SourceVpcLike []string
	NotSourceVpcLike []string
	Other map[string]interface{}
}


// Referer
type Referer struct {
	AllowEmptyReferer bool `json:"allowEmptyReferer"`
	AllowTruncateQueryString bool `json:"allowTruncateQueryString"`
	TruncatePath bool `json:"truncatePath"`
	RefererList []string `json:"refererList"`
	RefererBlackList []string `json:"refererBlackList"`
}


// AccessBlock
type AccessBlock struct {
	BlockPublicAcls bool `json:"blockPublicAcls" bson:"blockPublicAcls"`
	BlockPublicPolicy bool `json:"blockPublicPolicy" bson:"blockPublicPolicy"`
	IgnorePublicAcls bool `json:"ignorePublicAcls" bson:"ignorePublicAcls"`
	RestrictPublicBuckets bool `json:"restrictPublicBuckets" bson:"restrictPublicBuckets"`
	AccessAllBlock bool `json:"accessAllBlock" bson:"accessAllBlock"`
}


