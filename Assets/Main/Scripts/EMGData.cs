using System;
using System.Collections;
using System.Net.Sockets;
using System.Text;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class EMGData : MonoBehaviour
{

    private TcpClient client;
    private NetworkStream stream;
    private Rigidbody2D rb;
    private Collider2D coll;
    [SerializeField] private LayerMask jumpableGround;
    [SerializeField] private Text EmgVal;

    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        coll = GetComponent<Collider2D>();
        client = new TcpClient("localhost", 12345);
        stream = client.GetStream();

        StartCoroutine(ReadMessages());
    }
    IEnumerator ReadMessages()
    {
        byte[] data = new byte[1024];

        while (true)
        {
            if (stream.DataAvailable)
            {
                int bytesRead = stream.Read(data, 0, data.Length);
                string message = Encoding.UTF8.GetString(data, 0, bytesRead);

                string[] val = message.Split(',');
                foreach (var number in val)
                {
                    Debug.Log(number);
                    double jump = try_double(number);
                    if(jump > 0.0 && isGrounded())
                    {
                        rb.velocity = new Vector2(rb.velocity.x,12f);
                    }
                    // EmgVal.text = "EMG value : "+jump;
                }

                
            }

            yield return null;
        }
    }

    private double try_double(string v)
    {
        try
        {
            return double.Parse(v, System.Globalization.CultureInfo.InvariantCulture);
        } 
        catch
        {
            return 0.0;
        }
        
    }
        

    void OnApplicationQuit()
    {
        client.Close();
    }

    private bool isGrounded()
    {
        return Physics2D.BoxCast(coll.bounds.center, coll.bounds.size, 0f, Vector2.down, .1f, jumpableGround);
    }
}
