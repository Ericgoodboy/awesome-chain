
=== 结构体 Role 及其依赖定义 ===

// Role
type Role struct {
	Asset
	Region
	RoleInfo
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


// RoleInfo
type RoleInfo struct {
	RoleArn string `json:"roleArn" bson:"roleArn"`
	SubscriptionId string `json:"subscriptionId" bson:"subscriptionId"`
	PermissionBoundary string `json:"permissionBoundary" bson:"permissionBoundary"`
	PolicyIds []*PolicyBind `json:"policyIds" bson:"policyIds"`
	AssumeDocument *AcPolicyDocument `json:"assumeDocument" bson:"assumeDocument"`
	InlinePolicies []*AcPolicy `json:"inlinePolicies" bson:"inlinePolicies"`
	RoleName string `json:"roleName" bson:"roleName"`
}


// PolicyBind
type PolicyBind struct {
	// 策略id
	PolicyId string `json:"policyId" bson:"policyId"`
	// 作用的项目，为空表示全局作用(阿里云是资源组)
	ProjectId string `json:"projectId" bson:"projectId"`
}


// AcPolicyDocument
type AcPolicyDocument struct {
	Version string `json:"version" bson:"version"`
	Statements []*AcPolicyStatement `json:"statements" bson:"statements"`
}


// AcPolicyStatement
type AcPolicyStatement struct {
	Principal string `json:"principal" bson:"principal"`
	Effect EffectEnum `json:"effect" bson:"effect"`
	Action []string `json:"action" bson:"action"`
	NotAction []string `json:"notAction" bson:"notAction"`
	Resource []string `json:"resource" bson:"resource"`
	Condition string `json:"condition" bson:"condition"`
	NotResource []string `json:"notResource" bson:"notResource"`
	NotPrincipal string `json:"notPrincipal" bson:"notPrincipal"`
}


// AcPolicy
// 访问控制策略
type AcPolicy struct {
	Asset
	AcPolicyInfo
}


// AcPolicyInfo
type AcPolicyInfo struct {
	Type PolicyType `json:"type" bson:"type"`
	Version string `json:"version" bson:"version"`
	Document *AcPolicyDocument `json:"document" bson:"document"`
}


