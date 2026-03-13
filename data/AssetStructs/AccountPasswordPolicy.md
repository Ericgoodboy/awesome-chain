
=== 结构体 AccountPasswordPolicy 及其依赖定义 ===

// AccountPasswordPolicy
type AccountPasswordPolicy struct {
	Asset
	AccountPasswordPolicyInfo
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


// AccountPasswordPolicyInfo
type AccountPasswordPolicyInfo struct {
	RequireUppercaseCharacters bool ` json:"requireUppercaseCharacters" bson:"requireUppercaseCharacters"`
	RequireLowercaseCharacters bool `json:"requireLowercaseCharacters" bson:"requireLowercaseCharacters"`
	RequireNumbers bool `json:"requireNumbers" bson:"requireNumbers"`
	RequireSymbols bool `json:"requireSymbols" bson:"requireSymbols"`
	MinimumPasswordLength int32 `json:"minimumPasswordLength" bson:"minimumPasswordLength"`
	MaxPasswordAge int32 `json:"maxPasswordAge" bson:"maxPasswordAge"`
	PasswordReusePrevention int32 `json:"passwordReusePrevention" bson:"passwordReusePrevention"`
	AccountName string `json:"accountName" bson:"accountName"`
}


