resource "aws_route53_zone" "personal-site" {
  name = "kylesliva.me"
  comment = "Managed by Terraform"
  force_destroy = false
  tags = {
    "createdby" = "kylesliva"
  }
}

resource "aws_route53_record" "kylesliva_me_A" {
  zone_id = aws_route53_zone.personal-site.zone_id
  name = "kylesliva.me."
  type = "A"
  alias {
    name = "d3d874cdiuve6q.cloudfront.net."
    zone_id = "Z2FDTNDATAQYW2"
    evaluate_target_health = false
  }
  allow_overwrite = true
}

resource "aws_route53_record" "kylesliva_me_AAAA" {
  zone_id = aws_route53_zone.personal-site.zone_id
  name = "kylesliva.me."
  type = "AAAA"
  alias {
    name = "d3d874cdiuve6q.cloudfront.net."
    zone_id = "Z2FDTNDATAQYW2"
    evaluate_target_health = false
  }
  allow_overwrite = true
}

resource "aws_route53_record" "kylesliva_me_CAA" {
  zone_id = aws_route53_zone.personal-site.zone_id
  name = "kylesliva.me."
  type = "CAA"
  ttl = 3600
  records = [
    "0 issuewild \"amazon.com\"",
    "0 issue \"amazon.com\"",
  ]
  allow_overwrite = true
}

resource "aws_route53_record" "kylesliva_me_aws_acm_151e9ed2752c6da877e5e1c375bd344c_kylesliva_me_CNAME" {
  zone_id = aws_route53_zone.personal-site.zone_id
  name = "_151e9ed2752c6da877e5e1c375bd344c.kylesliva.me."
  type = "CNAME"
  ttl = 60
  records = [
    "_00368428d2c0cfdddebf8604ffa4f236.mhbtsbpdnt.acm-validations.aws.",
  ]
  allow_overwrite = true
}

resource "aws_route53_record" "kylesliva_me_minecraft_A" {
  zone_id = aws_route53_zone.personal-site.zone_id
  name = "minecraft.kylesliva.me."
  type = "A"
  ttl = 300
  records = [
    "3.142.139.68",
  ]
  allow_overwrite = true
}

resource "aws_route53_record" "kylesliva_me_www_A" {
  zone_id = aws_route53_zone.personal-site.zone_id
  name = "www.kylesliva.me."
  type = "A"
  alias {
    name = "d3d874cdiuve6q.cloudfront.net."
    zone_id = "Z2FDTNDATAQYW2"
    evaluate_target_health = false
  }
  allow_overwrite = true
}

resource "aws_route53_record" "kylesliva_me_www_AAAA" {
  zone_id = aws_route53_zone.personal-site.zone_id
  name = "www.kylesliva.me."
  type = "AAAA"
  alias {
    name = "d3d874cdiuve6q.cloudfront.net."
    zone_id = "Z2FDTNDATAQYW2"
    evaluate_target_health = false
  }
  allow_overwrite = true
}

