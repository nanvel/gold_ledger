import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();

const ami = aws.ec2
  .getAmi({
    filters: [
      {
        name: "name",
        values: ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-arm64-server-*"],
      },
    ],
    owners: ["099720109477"],
    mostRecent: true,
  })
  .then((result) => result.id);

const securityGroup = new aws.ec2.SecurityGroup("glSecurityGroup", {
  ingress: [
    {
      protocol: "tcp",
      fromPort: 80,
      toPort: 80,
      cidrBlocks: ["0.0.0.0/0"],
    },
    { protocol: "tcp", fromPort: 443, toPort: 443, cidrBlocks: ["0.0.0.0/0"] },
    { protocol: "tcp", fromPort: 22, toPort: 22, cidrBlocks: ["0.0.0.0/0"] },
  ],
  egress: [
    { protocol: "-1", fromPort: 0, toPort: 0, cidrBlocks: ["0.0.0.0/0"] },
  ],
});

const keyName = config.require("keyName");

const server = new aws.ec2.Instance("glServer", {
  tags: { Name: "glServer" },
  instanceType: aws.ec2.InstanceType.T4g_Medium,
  vpcSecurityGroupIds: [securityGroup.id],
  keyName: keyName,
  ami: ami,
});

const eip = new aws.ec2.Eip("glIP", { domain: "vpc" });

const eipAssociation = new aws.ec2.EipAssociation("glEipAssociation", {
  instanceId: server.id,
  allocationId: eip.id,
});

const domainName = config.require("domain");

const zone = new aws.route53.Zone("glZone", { name: domainName });

const wwwRecord = new aws.route53.Record("glRecordWww", {
  zoneId: zone.zoneId,
  name: domainName,
  type: "A",
  ttl: 300,
  records: [eip.publicIp],
});

export const serverIp = eip.publicIp;

const bucket = new aws.s3.Bucket("gold-ledger");

const glBucketOwnershipControls = new aws.s3.BucketOwnershipControls(
  "aclBucketOwnershipControls",
  {
    bucket: bucket.id,
    rule: {
      objectOwnership: "BucketOwnerPreferred",
    },
  },
);
const glBucketPublicAccessBlock = new aws.s3.BucketPublicAccessBlock(
  "aclBucketPublicAccessBlock",
  {
    bucket: bucket.id,
    blockPublicAcls: false,
    blockPublicPolicy: false,
    ignorePublicAcls: false,
    restrictPublicBuckets: false,
  },
);
const glBucketAclV2 = new aws.s3.BucketAclV2(
  "aclBucketAclV2",
  {
    bucket: bucket.id,
    acl: "private",
  },
  {
    dependsOn: [glBucketOwnershipControls, glBucketPublicAccessBlock],
  },
);

export const bucketName = bucket.id;

const serverUser = new aws.iam.User("glServerUser", {
  path: "/system/",
});

const userPolicyStatement = pulumi.interpolate`{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": ["s3:GetObject", "s3:PutObject", "s3:PutObjectAcl"],
      "Effect": "Allow",
      "Resource": ["${bucket.arn}/*"]
    }
  ]
}`;

const serverUserPolicy = new aws.iam.UserPolicy("serverUserPolicy", {
  user: serverUser.name,
  policy: userPolicyStatement,
});
