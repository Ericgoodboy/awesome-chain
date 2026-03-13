
=== 结构体 Account 及其依赖定义 ===

// Account
type Account struct {
	Asset
	Region
	AccountInfo
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


// AccountInfo
type AccountInfo struct {
	PasswordLastUsedTime time.Time
	RootUserId string
	AccessKeys []*AccessKey
	Policies []*Policy
	CredentialReport CredentialReportUser `json:"credentialReport"`
	SecurityAudit bool
	AttachPolicy bool
	AccessMode string
	ConsoleAccessEnabled bool `json:"consoleAccessEnabled" bson:"consoleAccessEnabled"`
	PolicyArns []string
	PolicyNames []string
	MfaConfig user.MfaConfig `json:"mfaConfig" bson:"mfaConfig"`
}


// AccessKey
type AccessKey struct {
	AccessKeyId string
	Status string
	CreateTime time.Time
	LastUsedTime time.Time
}


// Policy
type Policy struct {
	Name string
	PolicyId string
	Document
}


// Document
type Document struct {
	Statements []*Statement `json:"Statement"`
}


// Statement
type Statement struct {
	Effect EffectEnum `json:"Effect"`
	Action []string `json:"Action"`
	Resource []string `json:"Resource"`
}


// CredentialReportUser
type CredentialReportUser struct {
	User string `json:"user"`
	ARN string `json:"arn"`
	PasswordEnabled string `json:"password_enabled"`
	MFAActive string `json:"mfa_active"`
	PasswordLastUsed string `json:"password_last_used"`
	AccessKey1Active string `json:"access_key_1_active"`
	AccessKey2Active string `json:"access_key_2_active"`
	AccessKey1LastUsedDate string `json:"access_key_1_last_used_date"`
	AccessKey2LastUsedDate string `json:"access_key_2_last_used_date"`
	AccessKey1LastRotated string `json:"access_key_1_last_rotated"`
	AccessKey2LastRotated string `json:"access_key_2_last_rotated"`
}


